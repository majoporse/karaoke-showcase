from typing import List, Optional
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from domain import Lyrics as DomainLyrics
from domain.lyrics_chunk import LyricsChunk as DomainLyricsChunk
from domain.processing_result import (
    ProcessingResultUpdate as DomainProcessingResultUpdate,
)
from services.processing_result_service import ProcessingResultService

from .common import LyricsChunk, ProcessingResultResponse


class LyricsUpdate(BaseModel):
    full_text: Optional[str] = None
    chunks: Optional[List[LyricsChunk]] = None
    language: Optional[str] = None
    confidence_score: Optional[float] = None
    title: Optional[str] = None
    creator: Optional[str] = None
    duration_seconds: Optional[int] = None
    thumbnail_url: Optional[str] = None

    def to_domain(self, id: UUID) -> DomainLyrics:
        data = self.model_dump(exclude_unset=True)
        if self.chunks is not None:
            data["chunks"] = [
                DomainLyricsChunk(start=c.start, end=c.end, text=c.text)
                for c in self.chunks
            ]
        return DomainLyrics(processing_id=id, **data)


class ProcessingResultUpdate(BaseModel):
    youtube_url: Optional[str] = None
    youtube_video_id: Optional[str] = None
    title: Optional[str] = None
    uploader: Optional[str] = None
    uploader_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail: Optional[str] = None
    vocals_minio_path: Optional[str] = None
    accompaniment_minio_path: Optional[str] = None
    error_message: Optional[str] = None
    lyrics: Optional[LyricsUpdate] = None

    def to_domain(self, id: UUID) -> DomainProcessingResultUpdate:
        data = self.model_dump(exclude_unset=True)
        return DomainProcessingResultUpdate(id=id, **data)


router = APIRouter(
    prefix="/processing-results", tags=["Processing Results"], route_class=DishkaRoute
)


@router.put("/{result_id}", response_model=ProcessingResultResponse)
async def update_result(
    result_id: UUID,
    service: FromDishka[ProcessingResultService],
    request: ProcessingResultUpdate,
):
    updated = await service.update_result(result_id, request.to_domain(result_id))

    if not updated:
        raise HTTPException(status_code=404, detail="Processing result not found")

    return ProcessingResultResponse.from_domain(updated)
