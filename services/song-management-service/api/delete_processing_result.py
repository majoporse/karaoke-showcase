from fastapi import APIRouter
from pydantic import BaseModel
from dishka.integrations.fastapi import DishkaRoute
from services.processing_result_service import ProcessingResultService
from fastapi import HTTPException
from dishka.integrations.fastapi import FromDishka
from uuid import UUID


class DeleteResponse(BaseModel):
    message: str


router = APIRouter(
    prefix="/processing-results", tags=["Processing Results"], route_class=DishkaRoute
)


@router.delete("/{result_id}", response_model=DeleteResponse)
async def delete_result(result_id: UUID, service: FromDishka[ProcessingResultService]):
    success = await service.delete_result(result_id)
    if not success:
        raise HTTPException(status_code=404, detail="Processing result not found")
    return {"message": "Processing result deleted successfully"}
