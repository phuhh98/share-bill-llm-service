
from fastapi import APIRouter, status

from app.dtos.responses import BaseResponse

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
)
async def healthCheck():
    return BaseResponse(message="ok", status=status.HTTP_200_OK, data={})
