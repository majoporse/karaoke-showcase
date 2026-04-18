from typing import Optional, List, Generic, TypeVar
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from domain import Lyrics as DomainLyrics
from domain import ProcessingResult as DomainProcessingResult
from domain.files import get_accompaniment_path, get_vocal_path
from domain.lyrics_chunk import LyricsChunk as DomainLyricsChunk

T = TypeVar("T")


class LyricsChunk(BaseModel):
    start: float
    end: float
    text: str

    def to_domain(self):
        return DomainLyricsChunk(start=self.start, end=self.end, text=self.text)


class LyricsResponse(BaseModel):
    processing_id: UUID
    full_text: str
    chunks: List[LyricsChunk] = []
    language: str = "en"
    confidence_score: Optional[float] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, lyrics: DomainLyrics) -> "LyricsResponse":
        return cls(
            processing_id=lyrics.processing_id,
            full_text=lyrics.full_text,
            chunks=[
                LyricsChunk(start=c.start, end=c.end, text=c.text)
                for c in lyrics.chunks
            ]
            if lyrics.chunks
            else [],
            language=lyrics.language,
            confidence_score=lyrics.confidence_score,
        )


class ProcessingResultResponse(BaseModel):
    id: UUID
    youtube_url: str
    youtube_video_id: str
    title: str
    uploader: str
    uploader_url: str
    thumbnail_url: str
    thumbnail: str

    vocals_minio_path: str
    accompaniment_minio_path: str

    error_message: Optional[str] = None

    created_at: datetime
    lyrics: Optional[LyricsResponse] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, result: DomainProcessingResult) -> "ProcessingResultResponse":
        resp = cls(
            id=result.id,
            youtube_url=result.youtube_url,
            youtube_video_id=result.youtube_video_id,
            title=result.title,
            uploader=result.uploader,
            uploader_url=result.uploader_url,
            thumbnail_url=result.thumbnail_url,
            thumbnail=result.thumbnail,
            vocals_minio_path=get_vocal_path(result.id),
            accompaniment_minio_path=get_accompaniment_path(result.id),
            error_message=result.error_message,
            created_at=result.created_at,
            lyrics=LyricsResponse.from_domain(result.lyrics),
        )
        return resp

    @classmethod
    def from_domain_with_lyrics(
        cls, result: DomainProcessingResult
    ) -> "ProcessingResultResponse":
        return cls.from_domain(result)


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper"""

    items: List[T] = Field(description="List of items for this page")
    total: int = Field(description="Total number of items across all pages")
    page: int = Field(ge=1, description="Current page number (1-indexed)")
    limit: int = Field(ge=1, le=100, description="Number of items per page")
    total_pages: int = Field(ge=0, description="Total number of pages")

    @property
    def offset(self) -> int:
        """Calculate offset from page and limit"""
        return (self.page - 1) * self.limit

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        limit: int,
    ) -> "PaginatedResponse[T]":
        """Factory method to create paginated response"""
        total_pages = (total + limit - 1) // limit if total > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )
