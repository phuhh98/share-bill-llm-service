from typing import Any, Union

from pydantic import BaseModel

from .receipt import ParsedReceipt


class BaseResponse(BaseModel):
    data: Union[dict, str, Any, None] = None
    error: Union[dict, None] = None
    message: str
    status: int


class ReceiptData(BaseModel):
    receipt: ParsedReceipt


class ReceiptSuccessResponse(BaseResponse):
    data: ReceiptData
