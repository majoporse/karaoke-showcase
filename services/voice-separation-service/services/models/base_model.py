"""
Base model interface for voice separation models.
All voice separation models should inherit from this class.
"""

from abc import ABC, abstractmethod
from io import BytesIO
from typing import Tuple


class BaseSeparator(ABC):
    """Abstract base class for voice separation models."""

    def __init__(self):
        """Initialize the model."""
        self._initialized = False

    @abstractmethod
    def separate_vocals(self, audio_file: BytesIO) -> Tuple[BytesIO, BytesIO]:
        """
        Separate vocals from audio file.

        Args:
            audio_file: BytesIO object containing audio data

        Returns:
            Tuple of (vocals_file, accompaniment_file) as BytesIO objects
        """
        pass
