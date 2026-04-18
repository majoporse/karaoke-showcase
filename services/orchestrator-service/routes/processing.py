import logging
import traceback
import uuid
import json

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.song_management_service import ProcessingResponse, SongManagementService
from tasks.audio_processing_job import process_audio_job
from tasks.queue_tasks import queue, get_latest_message_key, redis_conn
from models.websocket_messages import ProcessingOutputMessage

logger = logging.getLogger(__name__)

processing_router = APIRouter(
    prefix="/process",
    tags=["Processing"],
    route_class=DishkaRoute,
)


class JobResponse(BaseModel):
    job_id: str


class QueuePositionResponse(BaseModel):
    task_id: str
    position: int | None
    total_in_queue: int


class LatestMessageResponse(BaseModel):
    job_id: str
    message: ProcessingOutputMessage | None


class SearchResultsResponse(BaseModel):
    items: list[ProcessingResponse]
    total: int


@processing_router.post(
    "/queue",
    response_model=JobResponse,
    summary="Queue audio processing from YouTube URL",
)
async def queue_audio_processing(youtube_url: str) -> JobResponse:
    logger.info(f"Queueing audio processing for {youtube_url}")

    try:
        custom_id = uuid.uuid4().hex
        job = queue.enqueue(
            process_audio_job,
            args=(youtube_url, custom_id),
            job_id=custom_id,
            job_timeout=60*15,
        )
        job_id = job.id

        logger.info(f"Job {job_id} enqueued successfully")
        return JobResponse(job_id=job_id)

    except Exception as e:
        logger.error(f"Failed to enqueue job: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@processing_router.get(
    "/search",
    response_model=SearchResultsResponse,
    summary="Search processing results by lyrics query",
)
async def search_results_by_query(
    query: str,
    song_service: FromDishka[SongManagementService],
    limit: int = 10,
    page: int = 0,
) -> SearchResultsResponse:
    logger.info(f"Received query: {query}")

    try:
        result, total = await song_service.get_processing_result_by_lyrics_query(query, page=page, limit=limit)
        return SearchResultsResponse(items=result, total=total)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during processing: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise


@processing_router.get("/processing/{id}", response_model=ProcessingResponse)
async def get_processing_result_by_id(
    id: uuid.UUID,
    song_service: FromDishka[SongManagementService],
) -> ProcessingResponse:
    logger.info(f"Received id: {id}")

    try:
        result = await song_service.get_processing_result(id)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during processing: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise


@processing_router.get(
    "/queue/position/{task_id}",
    response_model=QueuePositionResponse,
    summary="Get the position of a task in the Redis queue",
)
async def get_queue_position(task_id: str) -> QueuePositionResponse:
    logger.info(f"Getting queue position for task_id: {task_id}")

    try:
        # Get all job IDs in the queue
        job_ids = queue.job_ids
        total_in_queue = len(job_ids)

        # Find the position of the task
        if task_id in job_ids:
            position = job_ids.index(task_id)
            logger.info(
                f"Task {task_id} is at position {position} in queue (total: {total_in_queue})"
            )
            return QueuePositionResponse(
                task_id=task_id,
                position=position,
                total_in_queue=total_in_queue,
            )
        else:
            logger.warning(f"Task {task_id} not found in queue")
            return QueuePositionResponse(
                task_id=task_id,
                position=None,
                total_in_queue=total_in_queue,
            )


    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get queue position: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@processing_router.get(
    "/job/{job_id}/latest-message",
    response_model=LatestMessageResponse,
    summary="Get the latest message from a job's progress stream for reconnection",
)
async def get_latest_job_message(job_id: str) -> LatestMessageResponse:
    logger.info(f"Getting latest message for job_id: {job_id}")

    try:
        latest_key = get_latest_message_key(job_id)
        message_data = redis_conn.get(latest_key)

        if message_data is None:
            logger.warning(f"No latest message found for job_id: {job_id}")
            return LatestMessageResponse(job_id=job_id, message=None)

        # Parse the JSON message
        message_json = message_data.decode()

        message_dict = json.loads(message_json)
        message = ProcessingOutputMessage(**message_dict)

        logger.info(
            f"Retrieved latest message for job {job_id}: {message.payload.desc}"
        )
        return LatestMessageResponse(job_id=job_id, message=message)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get latest message: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
