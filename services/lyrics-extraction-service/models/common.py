from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """
    Standard error response model.
    """

    detail: str = Field(
        ...,
        description="Error description",
        json_schema_extra={"example": "Invalid YouTube URL provided"},
    )
    error_code: Optional[str] = Field(
        default=None,
        description="Optional error code for programmatic handling",
        json_schema_extra={"example": "INVALID_URL"},
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the error occurred",
    )


class StatusResponse(BaseModel):
    """
    Simple status response for health checks and root endpoints.
    """

    status: str = Field(
        ...,
        description="Current status",
        json_schema_extra={"example": "running"},
    )
    message: str = Field(
        ...,
        description="Human-readable message",
        json_schema_extra={"example": "Lyrics Extraction Service"},
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp",
    )


class AudioFileMetadata(BaseModel):
    """
    Metadata about an audio file.
    """

    filename: str = Field(
        ...,
        description="Name of the audio file",
        json_schema_extra={"example": "song.mp3"},
    )
    content_type: str = Field(
        ...,
        description="MIME type of the file",
        json_schema_extra={"example": "audio/mpeg"},
    )
    size_bytes: Optional[int] = Field(
        default=None,
        description="File size in bytes",
        json_schema_extra={"example": 5242880},
    )
    duration_seconds: Optional[float] = Field(
        default=None,
        description="Duration of the audio in seconds",
        json_schema_extra={"example": 213.5},
    )
    sample_rate: Optional[int] = Field(
        default=None,
        description="Sample rate in Hz",
        json_schema_extra={"example": 44100},
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="When the error occurred"
    )
