import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.dtos.exceptions import AppException
from app.dtos.responses import BaseResponse
from app.routers import llm, root

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
if ENVIRONMENT == "dev":
    load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split("|")

tags_metadata = [
    {
        "name": "llm",
        "description": "Endpoints for interacting with Large Language Models (LLMs) to perform various tasks such as text generation, summarization, translation, and more.",
    },
    {
        "name": "root",
        "description": "Basic health check endpoint to verify that the service is running.",
    },
]

app = FastAPI(
    title="Share Bill LLM Service",
    description="A service to extract and analyze receipt data using LLM",
    version="0.0.2",
    contact={
        "name": "Huynh Hoai Phu",
        "email": "phuhh98@gmail.com",
        "github": "https://github.com/phuhh98",
    },
)

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
