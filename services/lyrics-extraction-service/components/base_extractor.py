"""
Abstract base class for lyrics extraction implementations.
"""

from abc import ABC, abstractmethod
from io import BytesIO

from models.lyrics import TranscriptionResult


class LyricsExtractorBase(ABC):
    """Abstract base class for all lyrics extractor implementations."""

    @abstractmethod
    def initialize_model(self) -> bool:
        """
        Initialize the speech recognition model.

        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """
        Check if the extractor is ready to process audio files.

        Returns:
            bool: True if the model is loaded and ready, False otherwise.
        """
        pass

    @abstractmethod
    def extract(self, file: BytesIO) -> TranscriptionResult:
        """
        Extract lyrics from an audio file.

        Args:
            file: BytesIO object containing audio data

        Returns:
            TranscriptionResult: Object containing extracted text and timestamp chunks
        """
        pass
