from typing import Callable

from fastapi import Request

from app.dtos import exceptions
from app.external_services import firebase


async def fireBaseUserTokenAuth(request: Request, call_next: Callable):
    """
    Middleware to validate the JWT bearer token.
    Using firebase userId token in authorization header with Bearer prefix.
    """
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise exceptions.UnauthorizedException(message="Unauthorized no auth")

    token = authorization.split("Bearer ")[1]

    try:
        await firebase.verifyUserToken(userIdToken=token)
    except:
        raise exceptions.UnauthorizedException(message="Unauthorized: Invalid token")

    # Pass the request to the next handler
    return await call_next(request)
