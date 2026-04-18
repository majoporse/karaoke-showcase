import logging
import nest_asyncio
import time
import threading

from redis import Redis
from rq import Worker
from opentelemetry import trace

from config import settings
from worker_otel_setup import initialize_otel

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def start_worker():
    """Start the RQ worker process."""
    logger.info("Starting RQ Worker...")
    nest_asyncio.apply()

    # Initialize OpenTelemetry
    initialize_otel()

    # Initialize Redis connection
    redis_conn = Redis.from_url(settings.REDIS_URL)

    # Create worker for the default queue
    worker = Worker(["default"], connection=redis_conn)

    logger.info(
        f"Worker listening on queue 'default' with Redis URL: {settings.REDIS_URL}"
    )

    # Start the worker
    worker.work(with_scheduler=False)


if __name__ == "__main__":
    start_worker()
