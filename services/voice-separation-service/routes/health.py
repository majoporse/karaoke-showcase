from fastapi import APIRouter

from services.unified_separation_service import separator



# Initialize router with prefix and tags
health_router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

# Initialize voice separator (shared with separation routes)


@health_router.get(
    "",
    summary="Health check",
    description="Check if the voice separation service is healthy and ready",
)
async def health_check():
    """
    Check service health and model readiness.

    Returns:
        dict: Health status with model loading information
    """
    return {"status": "healthy", "model_loaded": separator is not None}
