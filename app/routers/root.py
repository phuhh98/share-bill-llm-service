from typing import Annotated

from fastapi import APIRouter, Header, status

from app.dtos.responses import BaseResponse
from app.external_services import firebase

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
)
async def healthCheck(authorization: Annotated[str, Header()]):
    token = authorization.split("Bearer ")[1]
    result = await firebase.verifyUserToken(token)
    return BaseResponse(message="ok", status=status.HTTP_200_OK, data=result)
