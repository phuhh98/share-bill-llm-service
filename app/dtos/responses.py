from typing import Any, Union

from pydantic import BaseModel

from .receipt import ParsedReceipt


class BaseResponse(BaseModel):
    data: Union[dict, str, Any, None] = None
    error: Union[dict, None] = None
    message: str
    status: int


class BadRequestResponse(BaseResponse):
    data: None = None
    error: dict
    message: str
    status: int = 400


class UnauthorizedResponse(BaseResponse):
    data: None = None
    error: dict
    message: str
    status: int = 401


class ReceiptData(BaseModel):
    receipt: ParsedReceipt


class ReceiptSuccessResponse(BaseResponse):
    data: ReceiptData
    status: int = 200
