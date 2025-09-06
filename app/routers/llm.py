import asyncio
import os
import tempfile
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, UploadFile, status
from google.genai.types import File as GoogleFile

from app.dependencies import auth, fileUpload
from app.dtos.receipt import ParsedReceipt
from app.dtos.responses import (
    BadRequestResponse,
    BaseResponse,
    ReceiptSuccessResponse,
    UnauthorizedResponse,
)
from app.external_services import googleAI
from app.llm.chains import receiptExtractor
from app.llm.prompts.receiptExtractor import ImageMeta, mediaMessagesCompose

router = APIRouter(prefix="/llm")


ALLOWED_MIME_TYPES = [
    "image/png",
    "image/jpg",
    "image/jpeg",
    "image/webp",
    "image/heic",
    "image/heif",
]
MAX_ALLOWED_FILE_SIZE = 20


@router.post(
    "/receipt-extractor",
    status_code=status.HTTP_200_OK,
    response_model=ReceiptSuccessResponse,
    responses={
        400: {"model": BadRequestResponse},
        401: {"model": UnauthorizedResponse},
    },
    tags=["llm"],
    dependencies=[
        Depends(auth.authenticate_user),
        Depends(
            fileUpload.FileUploadValidation(ALLOWED_MIME_TYPES, MAX_ALLOWED_FILE_SIZE)
        ),
    ],
)
async def receiptExtractorHanlder(
    files: Annotated[
        List[UploadFile], File(description="List of receipt images to be analyzed")
    ],
):
    # uploaded_files = [googleAI.uploadFile(file) for file in files]
    # define list for updateload files
    uploadedFiles: List[GoogleFile] = []
    imageMeta: List[ImageMeta] = []

    # Define an async upload function to handle each file
    async def upload_file_async(file: UploadFile):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
            # Await the async read operation
            tmp_file.write(file.file.read())
            tmp_file.close()
            # Await the async file upload
            uploadResult = googleAI.client.files.upload(
                file=tmp_file_path, config={"mime_type": file.content_type}
            )
            os.remove(tmp_file_path)
            return uploadResult, file.content_type

    async def upload_task():
        # Use asyncio.gather to run all uploads concurrently
        upload_tasks = [upload_file_async(file) for file in files]
        results = await asyncio.gather(*upload_tasks)

        # Process results from concurrent uploads
        for uploadResult, content_type in results:
            uploadedFiles.append(uploadResult)
            imageMeta.append(
                ImageMeta(url=str(uploadResult.uri), mime_type=str(content_type))
            )

    # Define an async delete function
    async def delete_file_async(file: GoogleFile):
        # Await the async file delete
        googleAI.client.files.delete(name=file.name)

    async def cleanup_task():
        print("cleaning up", uploadedFiles)
        if len(uploadedFiles) == 0:
            return
        # Use asyncio.gather to run all deletions concurrently
        delete_tasks = [delete_file_async(file) for file in uploadedFiles]
        await asyncio.gather(*delete_tasks)

    try:
        await upload_task()

        print("imageMeta\n", imageMeta)

        mediaMessages = mediaMessagesCompose(
            [
                ImageMeta(url=str(meta.url), mime_type=str(meta.mime_type))
                for meta in imageMeta
            ]
        )

        result = await receiptExtractor.chain.ainvoke({"mediaMessage": mediaMessages})
        assert isinstance(result, ParsedReceipt)

        return BaseResponse(
            message="ok", status=status.HTTP_200_OK, data={"receipt": result}
        )

    finally:
        await cleanup_task()
