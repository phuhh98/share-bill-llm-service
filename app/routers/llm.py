
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.dependencies import auth
from app.dtos.responses import BaseResponse
from app.llm.chains import travelAssisstant

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
