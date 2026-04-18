from dataclasses import dataclass
from typing import List, Optional
import uuid

from pydantic import BaseModel, Field

from models.youtube import YouTubeVideoMetadata


class Chunk(BaseModel):
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


@dataclass
class VoiceSeparationFiles:
    zip_url: str
    vocals_url: Optional[str] = None
    accompaniment_url: Optional[str] = None


class ProcessingRequest(BaseModel):
    youtube_url: str = Field(
        ...,
        description="YouTube URL to process",
        json_schema_extra={"example": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
    )


class LyricsCreate(BaseModel):
    processing_id: uuid.UUID = Field(
        ...,
        description="Processing ID",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    full_text: str = Field(default=..., description="Full lyrics text")
    chunks: Optional[list[Chunk]] = Field(
        default=None, description="Lyrics chunks with timing"
    )
    language: Optional[str] = Field(default="en", description="Language code")
    confidence_score: Optional[float] = None


class ProgressUpdate(BaseModel):
    current_step: int = Field(
        ...,
        description="Current step number",
        json_schema_extra={"example": 1},
    )
    total_steps: int = Field(
        ...,
        description="Total number of steps",
        json_schema_extra={"example": 5},
    )
    message: str = Field(
        ...,
        description="Progress message",
        json_schema_extra={"example": "Fetching video metadata"},
    )


class ProcessingResult(BaseModel):
    success: bool = Field(
        ...,
        description="Whether the processing was successful",
        json_schema_extra={"example": True},
    )
    message: str = Field(
        ...,
        description="Status message",
        json_schema_extra={"example": "Processing completed successfully"},
    )
    vocals_path: Optional[str] = Field(
        default=None,
        description="Download URL for extracted vocals track (MP3 format, 128kbps)",
        json_schema_extra={"example": "/download/vocals.mp3"},
    )
    accompaniment_path: Optional[str] = Field(
        default=None,
        description="Download URL for accompaniment track (music without vocals, MP3 format, 128kbps)",
        json_schema_extra={"example": "/download/accompaniment.mp3"},
    )
    lyrics: Optional[str] = Field(
        default=None,
        description="Full transcribed lyrics as plain text",
        json_schema_extra={
            "example": "Never gonna give you up\nNever gonna let you down"
        },
    )
    chunks: Optional[List[Chunk]] = Field(
        default=None,
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
    error: Optional[str] = Field(
        default=None,
        description="Error message if processing failed",
        json_schema_extra={"example": "Invalid YouTube URL"},
    )
    yt_metadata: Optional[YouTubeVideoMetadata] = Field(
        default=None,
        description="YouTube video metadata",
        json_schema_extra={
            "example": {"title": "Rick Astley - Never Gonna Give You Up"}
        },
    )
