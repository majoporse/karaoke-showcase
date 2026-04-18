import logging
import traceback
from io import BytesIO

from config import Config, load_config
from models.lyrics import TranscriptionResult

from .base_extractor import LyricsExtractorBase
from .stable_ts_aligner import StableTSAligner

logger = logging.getLogger(__name__)


class FasterWhisperExtractor(LyricsExtractorBase):
    def __init__(
        self,
        config: Config | None = None,
    ):
        if config is None:
            try:
                config = load_config()
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}, using defaults")
                config = Config()

        self.config = config
        self.aligner = StableTSAligner(
            config=self.config,
        )
        self.model_loaded = self.aligner.is_ready()

    def initialize_model(self) -> bool:
        try:
            logger.info("Initializing Stable-TS model for lyrics extraction...")
            self.aligner.initialize()
            is_ready = self.aligner.is_ready()
            if is_ready:
                self.model_loaded = True
                logger.info("Stable-TS model initialized successfully")
            return is_ready
        except Exception as e:
            logger.error(f"Failed to initialize Stable-TS model: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return False

    def is_ready(self) -> bool:
        return self.model_loaded

    def extract(self, file: BytesIO) -> TranscriptionResult:
        try:
            file.seek(0)
            bytes_data = file.read()

            logger.info("Using stable-ts with faster-whisper for transcription...")
            result = self.aligner.transcribe(bytes_data)

            if result is None:
                logger.error("No transcription result")
                return TranscriptionResult(text="", chunks=[])

            full_text, lyric_chunks = result

            if lyric_chunks:
                logger.info(
                    f"Successfully extracted {len(lyric_chunks)} lyric chunks with stable-ts"
                )
                return TranscriptionResult(text=full_text, chunks=lyric_chunks)
            else:
                logger.warning("No chunks extracted from audio, returning text only")
                return TranscriptionResult(text=full_text, chunks=[])

        except Exception as e:
            logger.error(f"Error extracting lyrics: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return TranscriptionResult(text="", chunks=[])
