"""
Health Check Routes.

Health monitoring for the lyrics extraction service.
"""

from fastapi import APIRouter

from routes.lyrics import extractor

# Initialize router with prefix and tags
health_router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@health_router.get(
    "",
    summary="Health check",
    description="Check if the lyrics extraction service is healthy and model is loaded",
)
async def health_check():
    """
    Check service health and model readiness.

    Returns:
        dict: Health status with model loading information
    """
    return {"status": "healthy", "model_loaded": extractor.is_ready()}
