from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.dtos.exceptions import AppException
from app.dtos.responses import BaseResponse
from app.routers import root

app = FastAPI()

app.include_router(root.router)


@app.exception_handler(Exception)
async def unicorn_exception_handler(_: Request, exc: Exception):
    if isinstance(exc, AppException):
        content = BaseResponse(
            status=exc.status_code, message=exc.message, error=exc.errorDetail
        ).model_dump(mode="json")
        return JSONResponse(content, status_code=exc.status_code)
    return JSONResponse(
        status_code=500,
        content={"error_msg": "Internal Server Error"},
    )
