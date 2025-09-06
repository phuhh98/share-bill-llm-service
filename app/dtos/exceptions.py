from typing import Any

from fastapi import status


class AppException(Exception):
    def __init__(self, status_code: int, message: str, errorDetail: Any = None) -> None:
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.errorDetail = errorDetail


class NotFoundException(AppException):
    def __init__(self, message: str, errorDetail: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            errorDetail=errorDetail,
        )


class BadRequestException(AppException):
    def __init__(self, message: str, errorDetail: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            errorDetail=errorDetail,
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str, errorDetail: Any = None) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            errorDetail=errorDetail,
        )
