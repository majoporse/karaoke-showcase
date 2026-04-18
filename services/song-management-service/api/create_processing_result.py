from typing import List, Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from pydantic import BaseModel

from domain import LyricsCreate as DomainLyricsCreate
from domain.processing_result import (
    ProcessingResultCreate as DomainProcessingResultCreate,
)
from services.processing_result_service import ProcessingResultService

from .common import LyricsChunk, ProcessingResultResponse


class LyricsCreate(BaseModel):
    full_text: str
    chunks: List[LyricsChunk] = []
    language: str = "en"
    confidence_score: Optional[float] = None

    def to_domain(self) -> DomainLyricsCreate:
        return DomainLyricsCreate(
            full_text=self.full_text,
            chunks=[c.to_domain() for c in self.chunks],
            language=self.language,
            confidence_score=self.confidence_score,
        )


class ProcessingResultCreate(BaseModel):
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
    lyrics: LyricsCreate

    def to_domain(self) -> DomainProcessingResultCreate:
        return (
            DomainProcessingResultCreate(
                youtube_url=self.youtube_url,
                youtube_video_id=self.youtube_video_id,
                title=self.title,
                uploader=self.uploader,
                uploader_url=self.uploader_url,
                thumbnail_url=self.thumbnail_url,
                thumbnail=self.thumbnail,
                vocals_minio_path=self.vocals_minio_path,
                accompaniment_minio_path=self.accompaniment_minio_path,
                error_message=self.error_message,
                lyrics=self.lyrics.to_domain()
            )
        )


router = APIRouter(
    prefix="/processing-results", tags=["Processing Results"], route_class=DishkaRoute
)


@router.post("/", response_model=ProcessingResultResponse, status_code=201)
async def create_result(
    service: FromDishka[ProcessingResultService],
    request: ProcessingResultCreate,
):
    proc_create = request.to_domain()
    created_result = await service.create_result(proc_create)
    return ProcessingResultResponse.from_domain(created_result)
