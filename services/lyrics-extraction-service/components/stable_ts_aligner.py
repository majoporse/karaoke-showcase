import logging
from typing import List

import stable_whisper
from faster_whisper import WhisperModel

from components.audio_chunker import AudioChunk, AudioChunker
from config import Config
from models.lyrics import Chunk

logger = logging.getLogger(__name__)


class StableTSAligner:
    model: WhisperModel

    def __init__(
        self,
        config: Config | None = None,
    ):
        self.config = config or Config()

        self.chunk_duration = self.config.chunk_duration
        self.loaded = False
        self.chunker = AudioChunker(
            chunk_duration=self.config.chunk_duration,
            overlap_duration=self.config.overlap_duration,
        )

    def initialize(self):
        try:
            logger.info(
                f"Loading stable-whisper with faster-whisper backend: {self.config.model_size}"
            )
            self.model = stable_whisper.load_faster_whisper(
                self.config.model_size,
                device=self.config.device,
                compute_type=self.config.compute_type,
            )
            self.loaded = True
            logger.info("Stable-TS with faster-whisper loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load stable-whisper: {str(e)}")
            self.loaded = False

    def is_ready(self) -> bool:
        return self.loaded

    def transcribe(
        self, audio: bytes, initial_prompt: str | None = None
    ) -> tuple[str, List[Chunk]] | None:
        """Returns (full_text, word_timestamps, lyric_chunks)"""
        if not self.loaded:
            logger.error("Stable-TS model not loaded")
            return None

        try:
            # Process all audio chunks and get WhisperResult
            audio_chunks = self._chunk_audio(audio)
            whisper_results = self._process_chunks_to_whisper_results(
                audio_chunks, initial_prompt=initial_prompt
            )
            filtered_segments = self._filter_results(whisper_results, audio_chunks)

            lyric_chunks = self._map_whisper_segments_to_chunks(filtered_segments)

            full_text = " ".join([seg.text for seg in filtered_segments])

            logger.info(
                f"Transcription complete: {len(full_text)} characters, "
                f"{len(lyric_chunks)} lyric chunks"
            )

            return full_text, lyric_chunks

        except Exception as e:
            logger.error(f"Error transcribing with stable-ts: {str(e)}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    def _chunk_audio(self, audio: bytes) -> List[AudioChunk]:
        logger.info(f"Chunking audio with {self.chunk_duration}s chunks...")
        audio_chunks = self.chunker.chunk_audio(audio)
        logger.info(f"Created {len(audio_chunks)} audio chunks")
        return audio_chunks

    def do_transcription(self, chunk_bytes: bytes):
        return self.model.transcribe(
            audio=chunk_bytes,
            verbose=self.config.verbose,
            log_progress=self.config.log_progress,
            vad=False,
            vad_threshold=self.config.vad_threshold,
            # repetition_penalty=0.95,
            condition_on_previous_text=False,
            temperature=0,
            q_levels=1,
            length_penalty=1.5,
            suppress_tokens=[],
            suppress_blank=False,
            # beam_size=20,
            patience=3,  # important for preventing skipping parts of songs
            # language_detection_segments=3,
            # language="sk",
            # compression_ratio_threshold=None,
            # log_prob_threshold=None,
            # no_speech_threshold=None,
        )

    def _process_chunks_to_whisper_results(
        self, audio_chunks: List[AudioChunk], initial_prompt: str | None = None
    ) -> List[stable_whisper.WhisperResult]:
        """Process each audio chunk and return list of WhisperResults."""
        results = []
        text = ""

        for chunk in audio_chunks:
            try:
                logger.info(
                    f"Transcribing chunk {chunk.chunk_index}: "
                    f"{chunk.start_time:.2f}s - {chunk.end_time:.2f}s"
                )

                chunk_bytes = chunk.to_bytes()

                result: stable_whisper.WhisperResult = self.do_transcription(
                    chunk_bytes
                )

                print(result.segments)

                for segment in result.segments:
                    segment.start += chunk.start_time
                    segment.end += chunk.start_time

                results.append(result)

            except Exception as chunk_error:
                logger.error(
                    f"Error transcribing chunk {chunk.chunk_index}: {str(chunk_error)}"
                )
                continue

        return results

    def _filter_results(
        self,
        results: List[stable_whisper.WhisperResult],
        audio_chunks: List[AudioChunk],
    ) -> List[stable_whisper.Segment]:
        """Merge multiple WhisperResults into a single result."""
        if not results:
            return []

        all_segments: List[stable_whisper.Segment] = []
        overlap_seconds = self.config.overlap_duration

        for index, result in enumerate(results):
            result_segments = [
                seg
                for seg in result.segments
                if (
                    index == len(audio_chunks) - 1
                    or index < len(audio_chunks) - 1
                    and seg.start <= audio_chunks[index + 1].start_time + 0.2
                    # and seg.end < audio_chunks[index].end_time
                )
                and (
                    index == 0
                    or index != 0
                    and seg.start > audio_chunks[index].start_time + 0.2
                )
            ]
            # print all segments
            print(f"Chunk {index}: {len(result_segments)} segments")
            print(result_segments)
            for segment in result_segments:
                print(segment)
            all_segments.extend(result_segments)

        all_segments.sort(key=lambda seg: seg.start)

        return all_segments

    def _map_whisper_segments_to_chunks(
        self, segments: List[stable_whisper.Segment]
    ) -> List[Chunk]:
        chunks = []

        for segment in segments:
            chunks.append(
                Chunk(start=segment.start, end=segment.end, text=segment.text.strip())
            )

        return chunks
