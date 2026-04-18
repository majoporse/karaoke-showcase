import logging

from lyrics_client.models.lyrics_with_timestamps_response import (
    LyricsWithTimestampsResponse,
)
from config import Settings
import lyrics_client
from lyrics_client import LyricsExtractionApi, ApiClient as LyricsClient

logger = logging.getLogger(__name__)


class LyricsExtractionService:
    def __init__(self, settings: Settings):
        self.configuration = lyrics_client.Configuration(
            host=settings.LYRICS_EXTRACTION_URL
        )

    async def extract_lyrics(
        self, tmp_path: str
    ) -> LyricsWithTimestampsResponse:
        logger.info(f"Extracting lyrics from {tmp_path}")

        try:
            with LyricsClient(self.configuration) as api_client:
                api_instance = LyricsExtractionApi(api_client)

                response = api_instance.extract_lyrics_with_timestamps_extract_lyrics_with_timestamps_post(
                    minio_path=tmp_path,
                )
                return response

        except lyrics_client.ApiException as e:
            logger.error(f"Lyrics extraction API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in lyrics extraction: {e}")
            return None
