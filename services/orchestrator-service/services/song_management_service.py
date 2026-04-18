import logging
import uuid
from datetime import datetime
from typing import Optional, Union, cast

from lyrics_client import LyricsWithTimestampsResponse
from pydantic import BaseModel
from song_management_client import ApiClient as SongManagementClient
from song_management_client import Configuration as SongManagementConfiguration
from song_management_client import (
    LyricsChunk,
    LyricsCreate,
    ProcessingResultCreate,
    ProcessingResultResponse,
    ProcessingResultsApi,
)
from song_management_client import LyricsChunk as SongManagementLyricsChunk

from config import Settings
from models.processing import Chunk
from models.youtube import YouTubeVideoMetadata
from services.minio_service import MinIOService

logger = logging.getLogger(__name__)


class Lyrics(BaseModel):
    processing_id: uuid.UUID
    full_text: str
    chunks: Optional[list[Chunk]] = None
    language: Optional[str] = "en"
    confidence_score: Optional[Union[float, int]] = None


class ProcessingResponse(BaseModel):
    youtube_url: Optional[str] = None
    youtube_video_id: Optional[str] = None
    title: Optional[str] = None
    uploader: Optional[str] = None
    uploader_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail: Optional[str] = None
    vocals_minio_path: Optional[str] = None
    accompaniment_minio_path: Optional[str] = None
    lyrics: Optional[Lyrics] = None
    error_message: Optional[str] = None
    id: uuid.UUID
    created_at: Optional[datetime] = None

    @staticmethod
    def from_song_service_response(processing_response: ProcessingResultResponse):

        lyrics = processing_response.lyrics
        if lyrics is None:
            raise ValueError("Lyrics are missing")

        chunks = cast(list[Chunk] | None, lyrics.chunks)
        chunks = (
            [
                Chunk(start=chunk.start, end=chunk.end, text=chunk.text)
                for chunk in chunks
            ]
            if lyrics and chunks
            else []
        )

        lyrics = Lyrics(
            processing_id=lyrics.processing_id,
            full_text=lyrics.full_text,
            chunks=chunks,
            language=lyrics.language,
            confidence_score=lyrics.confidence_score,
        )

        return ProcessingResponse(
            youtube_url=processing_response.youtube_url,
            youtube_video_id=processing_response.youtube_video_id,
            title=processing_response.title,
            uploader=processing_response.uploader,
            uploader_url=processing_response.uploader_url,
            thumbnail_url=processing_response.thumbnail_url,
            thumbnail=processing_response.thumbnail,
            vocals_minio_path=processing_response.vocals_minio_path,
            accompaniment_minio_path=processing_response.accompaniment_minio_path,
            lyrics=lyrics,
            error_message=processing_response.error_message,
            id=processing_response.id,
            created_at=processing_response.created_at,
        )


class SongManagementService:
    VOCALS_FILENAME = "vocals.mp3"
    ACCOMPANIMENT_FILENAME = "accompaniment.mp3"

    def __init__(self, minio_service: MinIOService, settings: Settings):
        self.minio = minio_service
        self.configuration = SongManagementConfiguration(
            host=settings.SONG_MANAGEMENT_URL
        )

    async def create_processing(
        self,
        youtube_url: str,
        vocals_path: str,
        accompaniment_path: str,
        lyrics_response: LyricsWithTimestampsResponse,
        video_metadata: Optional[YouTubeVideoMetadata] = None,
    ) -> ProcessingResponse:

        try:
            with SongManagementClient(self.configuration) as api_client:
                api_instance = ProcessingResultsApi(api_client)

                results_create = self.map_results_create(
                    lyrics_response,
                    vocals_path,
                    accompaniment_path,
                    youtube_url,
                    video_metadata,
                )
                api_response = api_instance.create_result_processing_results_post(
                    results_create,
                    _request_timeout=60 * 10,
                )

                return ProcessingResponse.from_song_service_response(api_response)

        except Exception as e:
            logger.error(f"Failed to create song entry: {e}")
            raise

    async def get_processing_result(self, result_id: uuid.UUID) -> ProcessingResponse:

        with SongManagementClient(self.configuration) as api_client:
            api_instance = ProcessingResultsApi(api_client)
            try:
                api_response = api_instance.get_result_processing_results_result_id_get(
                    result_id
                )
                return ProcessingResponse.from_song_service_response(api_response)

            except Exception as e:
                logger.error(f"Failed to get processing result: {e}")
                raise

    async def get_processing_result_by_lyrics_query(
        self, lyrics_query: str, limit: int = 10, page: int = 0
    ) -> tuple[list[ProcessingResponse], int]:
        with SongManagementClient(self.configuration) as api_client:
            api_instance = ProcessingResultsApi(api_client)
            try:
                api_response = (
                    api_instance.search_processing_results_processing_results_get(
                        lyrics_query, page=page, limit=limit
                    )
                )
                return [
                    ProcessingResponse.from_song_service_response(response)
                    for response in api_response.items
                ], api_response.total

            except Exception as e:
                logger.error(f"Failed to get processing result by id: {e}")
                raise

    def map_results_create(
        self,
        lyrics_response: LyricsWithTimestampsResponse,
        vocals_path: str,
        accompaniment_path: str,
        youtube_url: str,
        video_metadata: Optional[YouTubeVideoMetadata],
    ) -> ProcessingResultCreate:
        if not video_metadata:
            raise ValueError("Video metadata is required")

        return ProcessingResultCreate(
            youtube_url=youtube_url,
            youtube_video_id=video_metadata.id,
            title=video_metadata.title,
            uploader=video_metadata.uploader,
            uploader_url=video_metadata.uploader_url,
            thumbnail_url=video_metadata.thumbnail_url,
            thumbnail=video_metadata.thumbnail,
            vocals_minio_path=vocals_path,
            accompaniment_minio_path=accompaniment_path,
            lyrics=LyricsCreate(
                full_text=lyrics_response.text,
                chunks=[
                    LyricsChunk(start=chunk.start, end=chunk.end, text=chunk.text)
                    for chunk in cast(list[Chunk], lyrics_response.chunks)
                ],
            ),
        )

    def map_chunks(self, chunks: list[Chunk]) -> list[SongManagementLyricsChunk]:
        return [SongManagementLyricsChunk(**chunk.model_dump()) for chunk in chunks]
