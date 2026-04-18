import json
import logging

import redis.asyncio as aioredis
from chanx.core.decorators import channel, ws_handler
from chanx.fast_channels.websocket import AsyncJsonWebsocketConsumer, ReceiveEvent
from chanx.messages.incoming import PingMessage
from chanx.messages.outgoing import PongMessage
from fast_channels.type_defs import WebSocketDisconnectEvent

from config import settings
from models.websocket_messages import (
    JobProgressSubscriptionMessage,
    ProcessingOutputMessage,
    ProcessingOutputPayload,
    ProcessingResult,
)
from tasks.queue_tasks import get_channel_name

logger = logging.getLogger(__name__)




@channel(
    name="job-progress",
    description="Real-time job progress updates from Redis queue. Subscribe with a job_id path parameter to receive live progress updates as the background job executes.",
    tags=["jobs"],
)
class JobProgressConsumer(AsyncJsonWebsocketConsumer[ReceiveEvent]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_id = None
        self.redis_client = None
        self.pubsub = None

    @ws_handler(
        summary="Handle ping requests",
        description="Simple ping-pong for connectivity testing",
        output_type=PongMessage,
    )
    async def handle_ping(self, _message: PingMessage) -> PongMessage:
        return PongMessage()

    @ws_handler(
        summary="Subscribe to job progress",
        description="Subscribe to real-time progress updates for a specific job. Validates job_id and establishes Redis pubsub connection to stream live progress events.",
        tags=["subscription"],
        output_type=ProcessingOutputMessage,
    )
    async def handle_job_progress_subscribe(
        self, _message: JobProgressSubscriptionMessage
    ) -> None:

        if not self.job_id:
            raise ValueError("Missing or invalid job_id in path")
        if not self.redis_client:
            raise ValueError("Redis client not initialized")
        if not self.pubsub:
            raise ValueError("Pubsub not initialized")

        try:
            await self.pubsub.subscribe(get_channel_name(self.job_id))

            async for msg in self.pubsub.listen():
                if msg is None:
                    continue

                msg_type = msg.get("type")

                if msg_type == "message":
                    try:
                        msg_data = msg.get("data")

                        if isinstance(msg_data, bytes):
                            progress_dict = json.loads(msg_data.decode())
                        else:
                            progress_dict = json.loads(str(msg_data))

                        progress_msg = ProcessingOutputMessage(**progress_dict)

                        await self.send_message(progress_msg)

                    except Exception as e:
                        logger.error(f"Error sending progress message: {str(e)}")

        except Exception as e:
            logger.error(f"Job progress subscription error: {str(e)}")
            await self.send_message(
                ProcessingOutputMessage(
                    payload=ProcessingOutputPayload(
                        current_step=0,
                        total_steps=0,
                        desc="Error in progress subscription",
                        result=ProcessingResult(
                            success=False,
                            error=str(e),
                        ),
                    )
                )
            )

    async def post_authentication(self) -> None:

        self.job_id = self.scope["path_params"]["job_id"]

        self.redis_client = await aioredis.from_url(settings.REDIS_URL)
        self.pubsub = self.redis_client.pubsub()

    async def websocket_disconnect(self, message: WebSocketDisconnectEvent) -> None:

        if not self.job_id:
            return

        if self.pubsub:
            await self.pubsub.unsubscribe(get_channel_name(self.job_id))
            await self.pubsub.close()
