import logging
from typing import Optional

import redis
from rq import Queue

from config import settings
from models.websocket_messages import (
    ProcessingOutputMessage,
    ProcessingOutputPayload,
    ProcessingResult,
)

logger = logging.getLogger(__name__)

redis_conn = redis.from_url(settings.REDIS_URL)
queue = Queue(connection=redis_conn)


def get_channel_name(job_id: str) -> str:
    return f"job_progress:{job_id}"


def get_latest_message_key(job_id: str) -> str:
    return f"job_progress_latest:{job_id}"


def publish_job_progress(
    job_id: str,
    current_step: int,
    total_steps: int,
    desc: str,
    result: Optional[ProcessingResult] = None,
) -> None:
    payload = ProcessingOutputPayload(
        current_step=current_step,
        total_steps=total_steps,
        desc=desc,
        result=result,
    )
    progress_msg = ProcessingOutputMessage(payload=payload)

    channel_name = get_channel_name(job_id)
    message_json = progress_msg.model_dump_json()

    # Publish to all subscribers
    redis_conn.publish(channel_name, message_json)

    # Store the latest message for reconnection purposes
    latest_key = get_latest_message_key(job_id)
    redis_conn.set(latest_key, message_json, ex=3600)  # Expire after 1 hour

    logger.info(f"Published progress to {channel_name}: {desc}")
