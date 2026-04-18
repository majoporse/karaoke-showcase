import logging
from io import BytesIO
from typing import BinaryIO, List

import librosa
import numpy as np
import soundfile as sf

logger = logging.getLogger(__name__)


class AudioChunk:
    def __init__(
        self,
        audio_data: np.ndarray,
        sr: int | float,
        start_time: float,
        end_time: float,
        chunk_index: int,
    ):
        self.audio_data = audio_data
        self.sr = int(sr)
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time
        self.chunk_index = chunk_index

    def to_bytes(self) -> bytes:
        """Convert audio chunk to bytes (WAV format)."""
        buffer = BytesIO()
        sf.write(buffer, self.audio_data, self.sr, format="WAV")
        buffer.seek(0)
        return buffer.getvalue()

    def to_file(self) -> BinaryIO:
        """Convert audio chunk to file-like object (BinaryIO, WAV format)."""
        buffer = BytesIO()
        sf.write(buffer, self.audio_data, self.sr, format="WAV")
        buffer.seek(0)
        return buffer

    def crop_duration(self, start: float, end: float) -> "AudioChunk":
        if start < 0:
            raise ValueError(f"Start time cannot be negative: {start}")
        if end > self.duration:
            raise ValueError(
                f"End time ({end}s) exceeds chunk duration ({self.duration}s)"
            )
        if start >= end:
            raise ValueError(f"Start time ({start}s) must be before end time ({end}s)")

        start_sample = int(start * self.sr)
        end_sample = int(end * self.sr)
        cropped_audio = self.audio_data[start_sample:end_sample]

        new_start_time = self.start_time + start
        new_end_time = self.start_time + end

        return AudioChunk(
            audio_data=cropped_audio,
            sr=self.sr,
            start_time=new_start_time,
            end_time=new_end_time,
            chunk_index=self.chunk_index,
        )

    def split_with_overlap(
        self, sub_chunk_duration: float, overlap_duration: float
    ) -> List["AudioChunk"]:
        if sub_chunk_duration <= 0:
            raise ValueError(
                f"Sub-chunk duration must be positive: {sub_chunk_duration}"
            )
        if overlap_duration < 0:
            raise ValueError(f"Overlap duration cannot be negative: {overlap_duration}")
        if overlap_duration >= sub_chunk_duration:
            raise ValueError(
                f"Overlap ({overlap_duration}s) must be less than sub-chunk duration ({sub_chunk_duration}s)"
            )

        if self.duration <= sub_chunk_duration:
            return [self]

        sub_chunks: List["AudioChunk"] = []
        stride = sub_chunk_duration - overlap_duration
        current_time = 0.0

        while current_time < self.duration:
            end_time = min(current_time + sub_chunk_duration, self.duration)
            sub_chunk = self.crop_duration(current_time, end_time)
            sub_chunks.append(sub_chunk)

            if end_time >= self.duration:
                break

            current_time += stride

        return sub_chunks


class AudioChunker:
    def __init__(self, chunk_duration: float = 30.0, overlap_duration: float = 1.0):
        self.chunk_duration = chunk_duration
        self.overlap_duration = overlap_duration

    def chunk_audio(self, audio_bytes: bytes, sr: int = 16000) -> List[AudioChunk]:
        try:
            # Load audio from bytes
            audio, sample_rate = librosa.load(
                BytesIO(audio_bytes), sr=int(sr), mono=True
            )

            sample_rate = int(sample_rate)
            total_duration = len(audio) / sample_rate
            logger.info(
                f"Loaded audio: {total_duration:.2f}s at {sample_rate}Hz, "
                f"size: {len(audio)} samples"
            )

            # If audio is smaller than chunk duration, return as single chunk
            if total_duration <= self.chunk_duration:
                logger.info(
                    "Audio is smaller than chunk duration, returning as single chunk"
                )
                chunk = AudioChunk(
                    audio_data=audio,
                    sr=sample_rate,
                    start_time=0.0,
                    end_time=total_duration,
                    chunk_index=0,
                )
                return [chunk]

            # Calculate chunk sizes in samples
            chunk_samples = int(self.chunk_duration * sample_rate)
            overlap_samples = int(self.overlap_duration * sample_rate)
            stride_samples = chunk_samples - overlap_samples

            chunks: List[AudioChunk] = []

            for chunk_index, start_sample in enumerate(
                range(0, len(audio), stride_samples)
            ):
                end_sample = min(start_sample + chunk_samples, len(audio))

                # Avoid creating very small final chunks
                if end_sample - start_sample < sample_rate * 5:  # Less than 5 seconds
                    if chunks:
                        logger.debug(
                            f"Skipping small final chunk ({(end_sample - start_sample) / sample_rate:.1f}s)"
                        )
                        break
                    else:
                        pass

                chunk_audio = audio[start_sample:end_sample]
                start_time = start_sample / sample_rate
                end_time = end_sample / sample_rate

                chunk = AudioChunk(
                    audio_data=chunk_audio,
                    sr=sample_rate,
                    start_time=start_time,
                    end_time=end_time,
                    chunk_index=chunk_index,
                )
                chunks.append(chunk)

                logger.info(
                    f"Chunk {chunk_index}: {start_time:.2f}s - {end_time:.2f}s "
                    f"({chunk.duration:.2f}s, {len(chunk_audio)} samples)"
                )

            logger.info(f"Split audio into {len(chunks)} chunks")
            return chunks

        except Exception as e:
            logger.error(f"Error chunking audio: {str(e)}")
            raise

    @staticmethod
    def adjust_timestamps_for_chunk(
        chunk_start_time: float, timestamps: List[dict]
    ) -> List[dict]:
        adjusted = []
        for ts in timestamps:
            adjusted.append(
                {
                    **ts,
                    "start": ts["start"] + chunk_start_time,
                    "end": ts["end"] + chunk_start_time,
                }
            )
        return adjusted
