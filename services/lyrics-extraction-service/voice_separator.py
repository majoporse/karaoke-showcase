import logging
import zipfile
from io import BytesIO

import librosa
import soundfile as sf

logger = logging.getLogger(__name__)


class VoiceSeparator:
    def __init__(self):
        self.separator = "ready"  # Demo mode indicator

    def is_ready(self) -> bool:
        """Check if voice separation service is ready."""
        return self.separator is not None

    def separate_vocals(self, file: BytesIO) -> bytes:
        """Separate vocals from audio file (demo implementation)."""
        logger.info(f"Starting voice separation for: {file}")

        try:
            # Load audio from BytesIO
            logger.info("Loading audio file with librosa")
            file.seek(0)
            audio, sr = librosa.load(file, sr=None)
            logger.info(f"Audio loaded: shape={audio.shape}, sample_rate={sr}")

            # Simple separation using frequency filtering (basic approach)
            if len(audio.shape) == 1:
                audio = audio.reshape(1, -1)

            # For demo purposes, create simple separation
            vocals = audio * 0.7  # Simulated vocal extraction
            accompaniment = audio * 0.3  # Simulated accompaniment

            logger.info("Writing separated tracks to memory")
            # Write separated tracks to BytesIO objects
            vocals_file = BytesIO()
            accompaniment_file = BytesIO()

            sf.write(vocals_file, vocals[0], sr)
            sf.write(accompaniment_file, accompaniment[0], sr)

            # Reset file pointers for reading
            vocals_file.seek(0)
            accompaniment_file.seek(0)

            logger.info("Separated tracks ready in memory")

            # Create ZIP file in memory
            logger.info("Creating ZIP file in memory")
            zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                zipf.writestr("vocals.wav", vocals_file.getvalue())
                zipf.writestr("accompaniment.wav", accompaniment_file.getvalue())

            zip_buffer.seek(0)
            zip_content = zip_buffer.getvalue()

            logger.info(
                f"Voice separation completed successfully, ZIP size: {len(zip_content)} bytes"
            )
            return zip_content

        except Exception as e:
            logger.error(f"Error during voice separation: {str(e)}", exc_info=True)
            raise
