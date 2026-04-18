
from typing import List, Optional

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """
    A segment of lyrics with timestamp range.
    """

    start: float = Field(
        ...,
        description="Start time of the segment in seconds",
        json_schema_extra={"example": 0.0},
    )
    end: float = Field(
        ...,
        description="End time of the segment in seconds",
        json_schema_extra={"example": 12.92},
    )
    text: str = Field(
        ...,
        description="Lyrics text for this segment",
        json_schema_extra={"example": "Wake up in the mornin' feelin' like P. Diddy"},
    )


class TranscriptionResult(BaseModel):
    """
    Complete transcription result from the pipeline.
    """

    text: str = Field(
        ...,
        description="Full transcribed text",
        json_schema_extra={"example": "Wake up in the mornin'..."},
    )
    chunks: List[Chunk] = Field(
        ...,
        description="List of transcribed segments with timestamps",
        json_schema_extra={
            "example": [
                {
                    "start": 0.0,
                    "end": 12.92,
                    "text": "Wake up in the mornin' feelin' like P. Diddy",
                }
            ]
        },
    )


class LyricsTimestamp(BaseModel):
    """
    A segment of lyrics with a timestamp.
    """

    timestamp: float = Field(
        ...,
        description="Start time of the segment in seconds",
        json_schema_extra={"example": 0.0},
    )
    text: str = Field(
        ...,
        description="Lyrics text for this segment",
        json_schema_extra={"example": "Never gonna give you up"},
    )


class LyricsExtractionRequest(BaseModel):
    """
    Request model for lyrics extraction.

    Note: This is a placeholder since file uploads use UploadFile directly.
    For OpenAPI documentation purposes, this shows the expected parameters.
    """

    audio_file: Optional[str] = Field(
        default=None,
        description="Audio file to extract lyrics from (mp3, wav, m4a, etc.)",
        json_schema_extra={"example": "song.mp3"},
    )


class LyricsExtractionResponse(BaseModel):
    """
    Response model for plain lyrics extraction.
    """

    text: str = Field(
        ...,
        description="Extracted lyrics as plain text",
        json_schema_extra={
            "example": "Never gonna give you up\nNever gonna let you down"
        },
    )
    duration_seconds: Optional[float] = Field(
        default=None,
        description="Duration of the audio in seconds",
        json_schema_extra={"example": 213.5},
    )
    sample_rate: int = Field(
        ...,
        description="Sample rate used for processing (Hz)",
        json_schema_extra={"example": 16000},
    )


class LyricsWithTimestampsResponse(BaseModel):
    """
    Response model for lyrics extraction with timestamps.
    """

    text: str = Field(
        ...,
        description="Full transcribed text",
        json_schema_extra={"example": "Never gonna give you up..."},
    )
    chunks: List[Chunk] = Field(
        ...,
        description="List of lyrics segments with timestamps",
        json_schema_extra={
            "example": [
                {
                    "start": 0.0,
                    "end": 3.5,
                    "text": "Never gonna give you up",
                },
                {
                    "start": 3.5,
                    "end": 7.0,
                    "text": "Never gonna let you down",
                },
            ]
        },
    )
    total_duration_seconds: Optional[float] = Field(
        default=None,
        description="Total duration of the audio in seconds",
        json_schema_extra={"example": 213.5},
    )
    sample_rate: int = Field(
        ...,
        description="Sample rate used for processing (Hz)",
        json_schema_extra={"example": 16000},
    )


