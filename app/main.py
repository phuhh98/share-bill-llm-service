import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.dtos.exceptions import AppException
from app.dtos.responses import BaseResponse
from app.routers import llm, root
from fastapi.middleware.cors import CORSMiddleware

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
if ENVIRONMENT == "dev":
    load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split("|")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(llm.router)


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
