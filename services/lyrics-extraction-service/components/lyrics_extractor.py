import logging
import traceback
from io import BytesIO

import librosa
import torch
from transformers import (
    BitsAndBytesConfig,
    pipeline,
)

from .base_extractor import LyricsExtractorBase
from models.lyrics import TranscriptionResult, Chunk

logger = logging.getLogger(__name__)


class LyricsExtractor(LyricsExtractorBase):
    def __init__(self):
        self.model_id = "openai/whisper-large-v3-turbo"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 4-bit quantization config
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )

        # Create pipeline with model_kwargs to pass quantization config
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model_id,
            torch_dtype=torch.float16,
            model_kwargs={
                "quantization_config": quantization_config,
                "device_map": "auto",
            },
        )
        self.model_loaded = True
        logger.info(
            f"loaded successfully model id:{self.model_id}, device:{self.device}"
        )

    def initialize_model(self):
        """Initialize the Whisper model for lyrics extraction."""
        try:
            logger.info("Initializing Whisper model for lyrics extraction...")

            logger.info(f"Whisper model loaded successfully on {self.device}")
            return True

        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            # Fallback to demo mode
            self.model_loaded = False
            logger.warning("Running in demo mode - model loading failed")
            return False

    def is_ready(self) -> bool:
        """Check if lyrics extraction service is ready."""
        return self.model_loaded

    def extract(self, file: BytesIO) -> TranscriptionResult:
        """Extract lyrics from audio file and return as structured data."""

        try:
            y, sr = librosa.load(file, sr=16000)
            result = self.pipe(y, return_timestamps=True)

            # Parse the pipeline result into our custom data class
            chunks = []
            print(result)
            for chunk in result.get("chunks", []):
                start, end = chunk["timestamp"]
                if start is None or end is None:
                    continue
                chunks.append(Chunk(start=start, end=end, text=chunk["text"]))

            transcription = TranscriptionResult(text=result["text"], chunks=chunks)

            logger.info(f"Successfully extracted {len(chunks)} chunks from audio")
            return transcription

        except Exception as e:
            logger.error(f"Error extracting lyrics: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return TranscriptionResult(text="", chunks=[])
