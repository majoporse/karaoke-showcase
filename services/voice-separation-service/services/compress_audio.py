import io
import logging

from pydub import AudioSegment

logger = logging.getLogger(__name__)


def compress_wav_to_mp3(wav_bytes: io.BytesIO, bitrate: str = "128k") -> bytes:
    try:
        logger.info(f"Compressing WAV to MP3 with bitrate {bitrate}")

        # Load WAV from bytes
        audio = AudioSegment.from_wav(wav_bytes)

        # Export to MP3
        mp3_buffer = io.BytesIO()
        audio.export(mp3_buffer, format="mp3", bitrate=bitrate)

        mp3_bytes = mp3_buffer.getvalue()

        # Calculate compression ratio
        original_size = len(wav_bytes.getvalue())
        compressed_size = len(mp3_bytes)
        compression_ratio = (1 - compressed_size / original_size) * 100

        logger.info(
            f"Compression complete: {original_size:,} bytes → {compressed_size:,} bytes "
            f"({compression_ratio:.1f}% reduction)"
        )

        return mp3_bytes

    except Exception as e:
        logger.error(f"Failed to compress WAV to MP3: {str(e)}")
        raise Exception(f"Audio compression failed: {str(e)}")
