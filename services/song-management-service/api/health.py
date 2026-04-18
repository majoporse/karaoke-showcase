from fastapi import APIRouter

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
    return {"status": "healthy"}
