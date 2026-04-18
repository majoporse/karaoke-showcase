import logging
import uuid

from lyrics_client import LyricsWithTimestampsResponse

from models.processing import Chunk
from models.youtube import YouTubeVideoMetadata
from services.minio_service import MinIOService
from services.youtube_downloader import YouTubeDownloader

from .lyrics_extraction_service import LyricsExtractionService
from .song_management_service import ProcessingResponse, SongManagementService
from .voice_separation_service import VoiceSeparationService

logger = logging.getLogger(__name__)


class ProcessingOrchestrator:
    def __init__(
        self,
        voice_separation_service: VoiceSeparationService,
        lyrics_extraction_service: LyricsExtractionService,
        song_management_service: SongManagementService,
        youtube_downloader: YouTubeDownloader,
        minio_client: MinIOService,
    ):
        self.voice_separation = voice_separation_service
        self.lyrics_extraction = lyrics_extraction_service
        self.song_management = song_management_service
        self.youtube_downloader = youtube_downloader
        self.minio = minio_client

    async def fetch_video_metadata(self, youtube_url: str) -> YouTubeVideoMetadata:
        return await self.youtube_downloader.get_metadata(youtube_url)

    async def download_audio(self, youtube_url: str) -> bytes:
        return await self.youtube_downloader.download_audio(youtube_url)

    async def separate_vocals(self, tmp_path: str) -> tuple[str, str]:
        res = await self.voice_separation.separate_audio(tmp_path)
        return res.vocals_path, res.accompaniment_path

    async def extract_lyrics(self, vocals_path: str) -> LyricsWithTimestampsResponse:
        lyrics_response = await self.lyrics_extraction.extract_lyrics(vocals_path)
        return lyrics_response

    async def store_processing_result(
        self,
        youtube_url: str,
        video_metadata: YouTubeVideoMetadata,
        vocals_path: str,
        accompaniment_path: str,
        lyrics_response: LyricsWithTimestampsResponse,
    ) -> ProcessingResponse:
        return await self.song_management.create_processing(
            youtube_url=youtube_url,
            video_metadata=video_metadata,
            vocals_path=vocals_path,
            accompaniment_path=accompaniment_path,
            lyrics_response=lyrics_response,
        )

    async def save_audio(self, audio_bytes: bytes) -> str:
        tmp_id = uuid.uuid4()
        tmp_path = f"tmp/{tmp_id}.mp3"

        self.minio.upload_file(audio_bytes, tmp_path)
        return tmp_path

    def _convert_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        return [
            Chunk(start=chunk.start, end=chunk.end, text=chunk.text) for chunk in chunks
        ]
