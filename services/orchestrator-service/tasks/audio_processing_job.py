import asyncio
import logging

from di import container
from models.websocket_messages import ProcessingResult
from services.minio_service import MinIOService
from services.orchestrator_service import ProcessingOrchestrator
from tasks.queue_tasks import publish_job_progress

logger = logging.getLogger(__name__)


def process_audio_job(job_id: str, youtube_url: str) -> None:
    asyncio.run(_process_audio_async(job_id, youtube_url))


async def _process_audio_async(youtube_url: str, job_id: str) -> None:
    orchestrator: ProcessingOrchestrator = await container.get(ProcessingOrchestrator)
    minio: MinIOService = await container.get(MinIOService)
    tmp_path = None
    accompaniment_path = None
    vocals_path = None

    try:
        publish_job_progress(job_id, 1, 5, "Fetching video metadata")
        logger.info(f"Fetching video metadata for {youtube_url}")
        video_metadata = await orchestrator.fetch_video_metadata(youtube_url)

        publish_job_progress(job_id, 2, 5, "Downloading audio")
        logger.info(f"Downloading audio for {youtube_url}")
        audio_bytes = await orchestrator.download_audio(youtube_url)

        logger.info(f"Saving audio for {youtube_url}")
        tmp_path = await orchestrator.save_audio(audio_bytes)

        publish_job_progress(job_id, 3, 5, "Separating vocals")
        logger.info(f"Separating vocals for {youtube_url}")
        vocals_path, accompaniment_path = await orchestrator.separate_vocals(tmp_path)

        publish_job_progress(job_id, 4, 5, "Extracting lyrics")
        logger.info(f"Extracting lyrics for {youtube_url}")
        lyrics_response = await orchestrator.extract_lyrics(tmp_path)

        publish_job_progress(job_id, 5, 5, "Storing processing result")
        logger.info(f"Storing processing result for {youtube_url}")
        processing_response = await orchestrator.store_processing_result(
            youtube_url=youtube_url,
            video_metadata=video_metadata,
            vocals_path=vocals_path,
            accompaniment_path=accompaniment_path,
            lyrics_response=lyrics_response,
        )

        result = ProcessingResult(
            success=True,
            vocals_path=processing_response.vocals_minio_path,
            accompaniment_path=processing_response.accompaniment_minio_path,
            lyrics=lyrics_response.text,
            chunks=processing_response.lyrics.chunks
            if processing_response.lyrics
            else None,
            yt_metadata=video_metadata,
        )

        publish_job_progress(
            job_id,
            5,
            5,
            "Processing completed successfully",
            result=result,
        )

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        publish_job_progress(
            job_id,
            0,
            5,
            "Processing failed",
            result=ProcessingResult(success=False, error=str(e)),
        )

    finally:
        if tmp_path:
            minio.remove_object(tmp_path)
        if accompaniment_path:
            minio.remove_object(accompaniment_path)
        if vocals_path:
            minio.remove_object(vocals_path)
