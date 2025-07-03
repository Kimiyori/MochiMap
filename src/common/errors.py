from fastapi import HTTPException


class BaseHttpException(HTTPException):
    def __init__(self, message: str, status_code: int):
        self._message = message

        super().__init__(status_code=status_code, detail=message)

    def __str__(self) -> str:
        return self._message


class BadRequestException(BaseHttpException):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401)


class UnsupportedMediaTypeException(HTTPException):
    def __init__(self):
        super().__init__(status_code=415)


class ForbiddenException(BaseHttpException):
    def __init__(self, message: str):
        super().__init__(message, status_code=403)


class NotFoundException(BaseHttpException):
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class ConflictException(BaseHttpException):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class InternalServerException(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=500)
        self.detail = detail

    def __str__(self):
        return self.detail
