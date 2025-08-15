from pydantic import BaseModel


class BaseErrorResponse(BaseModel):
    message: str
    error: str
    timestamp: str


class BaseRequestCommand(BaseModel):
    pass
