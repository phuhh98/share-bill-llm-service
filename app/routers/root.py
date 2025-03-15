from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from app.dependencies import auth
from app.dtos.responses import BaseResponse
from app.services import firebase

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
    dependencies=[Depends(auth.authenticate_user)],
)
async def healthCheck(authorization: Annotated[str, Header()]):
    token = authorization.split("Bearer ")[1]
    result = await firebase.verifyUserToken(token)
    return BaseResponse(message="ok", status=status.HTTP_200_OK, data=result)
