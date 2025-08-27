
import os
import tempfile
from typing import List

from fastapi import APIRouter, Depends, UploadFile, status
from google.genai.types import File as GoogleFile
from pydantic import BaseModel

from app.dependencies import auth
from app.dtos.responses import BaseResponse
from app.external_services import googleAI
from app.llm.chains import receiptExtractor, travelAssisstant
from app.llm.prompts.receiptExtractor import ImageMeta, mediaMessagesCompose

router = APIRouter(prefix="/llm")

class LLMQuestion(BaseModel):
    question: str

@router.post(
    "/travel-assistant",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
    dependencies=[Depends(auth.authenticate_user)],
)
async def travelAssistant(body: LLMQuestion):
    result = travelAssisstant.chain.invoke({"question": body.question})
    return BaseResponse(message="ok", status=status.HTTP_200_OK, data=result)



@router.post(
    "/receipt-extractor",
    status_code=status.HTTP_200_OK,
    response_model=BaseResponse,
    dependencies=[Depends(auth.authenticate_user)],
)
async def receiptExtractorHanlder(files: list[UploadFile]):
    # uploaded_files = [googleAI.uploadFile(file) for file in files]
    # define list for updateload files
    uploadedFiles: List[GoogleFile] = []
    imageMeta: List[ImageMeta] =[]
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
            tmp_file.write(file.file.read())  # Corrected line
            tmp_file.close()
            uploadResult = googleAI.client.files.upload(file=tmp_file_path, config={
                "mime_type": file.content_type
            })
            imageMeta.append(ImageMeta(url=str(uploadResult.uri), mime_type=str(file.content_type)))
            os.remove(tmp_file_path) # remove temp file

    print("imageMeta\n", imageMeta)
    mediaMessages = mediaMessagesCompose([ImageMeta(url=str(meta.url) , mime_type=str(meta.mime_type)) for meta in imageMeta])
    result = receiptExtractor.chain.invoke({
        "mediaMessage": mediaMessages 
# format_instructions : output Schema
# mediaMessage: Message compose from MediaMesage Class
    })

    return BaseResponse(message="ok", status=status.HTTP_200_OK, data={"receipt": result})
