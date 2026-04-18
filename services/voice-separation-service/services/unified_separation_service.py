import asyncio
import logging
import uuid
from io import BytesIO
from typing import Optional

from fastapi import UploadFile

from config import CONFIG
from config.settings import settings
from services.compress_audio import compress_wav_to_mp3
from services.minio_service import MinIOService
from services.models.base_model import BaseSeparator

logger = logging.getLogger(__name__)

separator: Optional[BaseSeparator] = None

if CONFIG.voice_separation.active_model == "demucs":
    from .models.demucs_model import DemucsSeparator

    separator = DemucsSeparator()

if CONFIG.voice_separation.active_model == "spleeter":
    from .models.spleeter_model import SpleeterSeparator

    separator = SpleeterSeparator()


def separate_vocals(minio_path: str) -> tuple[str, str]:

    try:
        if separator is None:
            raise ValueError("No separator model configured")
        minio = MinIOService(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
            bucket_name=settings.MINIO_BUCKET_NAME,
        )

        audio_bytes = minio.get_file(minio_path)

        vocals, instrumental = separator.separate_vocals(BytesIO(audio_bytes))
        vocals_compressed = compress_wav_to_mp3(vocals)
        instrumental_compressed = compress_wav_to_mp3(instrumental)

        tmp_id = uuid.uuid4()
        vocals_path = f"tmp/vocals-{tmp_id}.mp3"
        accompaniment_path = f"tmp/accompaniment-{tmp_id}.mp3"

        minio.upload_file(vocals_compressed, vocals_path)
        minio.upload_file(instrumental_compressed, accompaniment_path)

        return vocals_path, accompaniment_path

    except Exception as e:
        logger.error(
            f"Error separating voice with {CONFIG.voice_separation.active_model}: {e}"
        )
        raise
