"""
Models module for lyrics extraction service.

This module provides Pydantic models for the lyrics extraction service API.
"""

from .common import ErrorResponse, StatusResponse, AudioFileMetadata
from .lyrics import (
    LyricsExtractionRequest,
    LyricsExtractionResponse,
    LyricsTimestamp,
    LyricsWithTimestampsResponse,
)

__all__ = [
    "ErrorResponse",
    "StatusResponse",
    "AudioFileMetadata",
    "LyricsExtractionRequest",
    "LyricsExtractionResponse",
    "LyricsTimestamp",
    "LyricsWithTimestampsResponse",
]
