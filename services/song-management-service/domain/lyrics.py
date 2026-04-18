import uuid
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.lyrics_chunk import LyricsChunk


class Lyrics(BaseModel):
    processing_id: UUID
    full_text: str = ""
    chunks: Optional[List[LyricsChunk]] = Field(default_factory=list)
    language: str = "en"
    confidence_score: Optional[float] = None


class LyricsCreate(BaseModel):
    full_text: str = ""
    chunks: Optional[List[LyricsChunk]] = Field(default_factory=list)
    language: str = "en"
    confidence_score: Optional[float] = None

    def to_lyrics(self, processing_id: UUID) -> Lyrics:
        return Lyrics(
            processing_id=processing_id,
            full_text=self.full_text,
            chunks=self.chunks,
            language=self.language,
            confidence_score=self.confidence_score,
        )
