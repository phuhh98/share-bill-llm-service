from typing import Annotated, Union

from fastapi import Header

from app.dtos import exceptions
from app.services import firebase


async def authenticate_user(
    authorization: Annotated[Union[str, None], Header()] = None,
):
    if not authorization or not authorization.startswith("Bearer "):
        raise exceptions.UnauthorizedException(
            message="Unauthorized: authorization header is missing."
        )

    token = authorization.split("Bearer ")[1]

    if not token:
        raise exceptions.UnauthorizedException(message="Unauthorized: token is missing")

    try:
        await firebase.verifyUserToken(userIdToken=token)
    except:
        raise exceptions.UnauthorizedException(message="Unauthorized: Invalid token")
