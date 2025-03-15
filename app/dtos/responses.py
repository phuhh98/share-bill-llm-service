from typing import Any, Union

from pydantic import BaseModel


class BaseResponse(BaseModel):
    data: Union[dict, str, Any, None] = None
    error: Union[dict, None] = None
    message: str
    status: int
