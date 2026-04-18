from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from domain import Lyrics, LyricsCreate


class ProcessingResult(BaseModel):
    id: UUID

    youtube_url: str
    youtube_video_id: str
    title: str
    uploader: str
    uploader_url: str
    thumbnail_url: str
    thumbnail: str

    created_at: datetime
    error_message: Optional[str]

    lyrics: Lyrics


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

    error_message: Optional[str]
    lyrics: LyricsCreate


class ProcessingResultUpdate(BaseModel):
    id: UUID

    youtube_url: Optional[str]
    youtube_video_id: Optional[str]
    title: Optional[str]
    uploader: Optional[str]
    uploader_url: Optional[str]
    thumbnail_url: Optional[str]
    thumbnail: Optional[str]

    vocals_minio_path: Optional[str]
    accompaniment_minio_path: Optional[str]

    created_at: Optional[datetime]
    error_message: Optional[Optional[str]]
    lyrics: Optional[LyricsCreate]

