import os
import tempfile
from typing import Annotated, List

from fastapi import APIRouter, Depends, File, UploadFile, status
from google.genai.types import File as GoogleFile

from app.dependencies import auth, fileUpload
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
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
            tmp_file.write(file.file.read())  # Corrected line
            tmp_file.close()
            uploadResult = googleAI.client.files.upload(
                file=tmp_file_path, config={"mime_type": file.content_type}
            )
            uploadedFiles.append(uploadResult)
            imageMeta.append(
                ImageMeta(url=str(uploadResult.uri), mime_type=str(file.content_type))
            )
            os.remove(tmp_file_path)  # remove temp file

    print("imageMeta\n", imageMeta)
    mediaMessages = mediaMessagesCompose(
        [
            ImageMeta(url=str(meta.url), mime_type=str(meta.mime_type))
            for meta in imageMeta
        ]
    )
    result = receiptExtractor.chain.invoke({"mediaMessage": mediaMessages})

    return BaseResponse(
        message="ok", status=status.HTTP_200_OK, data={"receipt": result}
    )
