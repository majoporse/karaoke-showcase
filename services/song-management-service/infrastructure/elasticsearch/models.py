from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID


class LyricsChunk(BaseModel):
    start: float = Field(default=0.0, description="Start time in seconds")
    end: float = Field(default=0.0, description="End time in seconds")
    text: str = Field(default="", description="Text of the chunk")


class LyricsDocument(BaseModel):

    processing_id: UUID = Field(..., description="Unique identifier of the lyrics document")
    full_text: str = Field(..., description="Full lyrics text")
    chunks: List[LyricsChunk] = Field(
        default_factory=list, description="Lyrics chunks with timing"
    )
    language: str = Field(default="en", description="Language code")
    confidence_score: Optional[float] = Field(
        default=None, description="Confidence score of transcription"
    )
    last_updated: Optional[datetime] = Field(
        default=None, description="Last update timestamp"
    )
    # Metadata from source (e.g., YouTube)
    title: Optional[str] = Field(None, description="Song title")
    creator: Optional[str] = Field(None, description="Artist/Creator name")
    duration_seconds: Optional[int] = Field(None, description="Duration in seconds")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")

    class Config:
        from_attributes = True
        validate_by_name = True
