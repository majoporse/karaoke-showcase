from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from pydantic import BaseModel

from services.minio_service import MinIOService

storage_router = APIRouter(
    prefix="/presign",
    tags=["Storage"],
)


class PresignResponse(BaseModel):
    url: str


@storage_router.get(
    "",
    summary="Presign URL",
    description="Get a presigned URL for a file in the storage bucket",
    response_model=PresignResponse,
)
@inject
async def presign_url(
    key: str,
    minio: FromDishka[MinIOService],
):
    url = minio.get_presigned_url(key)
    return PresignResponse(url=url)
