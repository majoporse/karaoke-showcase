"""
Voice separation service for separating vocals from background music.
"""

import logging

import voice_separation_client
from pydantic import BaseModel
from voice_separation_client import ApiClient as VoiceSeparationClient
from voice_separation_client.api.voice_separation_api import VoiceSeparationApi

from config import Settings
from services.minio_service import MinIOService

logger = logging.getLogger(__name__)


class VoiceSeparationResult(BaseModel):
    vocals_path: str
    accompaniment_path: str


class VoiceSeparationService:
    def __init__(self, settings: Settings, minio: MinIOService):
        self.configuration = voice_separation_client.Configuration(
            host=settings.VOICE_SEPARATION_URL,
        )
        self.minio = minio

    async def separate_audio(self, tmp_path: str) -> VoiceSeparationResult:
        logger.info(f"Requesting voice separation for {tmp_path}")

        with VoiceSeparationClient(self.configuration) as api_client:
            api_instance = VoiceSeparationApi(api_client)

            api_response = api_instance.separate_voice_unified_separate_voice_post(
                minio_path=tmp_path,
            )

            return VoiceSeparationResult(
                vocals_path=api_response.vocals_path,
                accompaniment_path=api_response.accompaniment_path,
            )

