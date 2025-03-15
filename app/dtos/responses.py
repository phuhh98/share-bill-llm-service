from typing import Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    data: Union[dict, None] = None
    error: Union[dict, None] = None
    message: str
    status: int
