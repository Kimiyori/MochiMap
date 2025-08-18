from datetime import UTC, datetime
from typing import Annotated

from pydantic import BaseModel, Field, constr


class BaseErrorResponse(BaseModel):
    message: Annotated[str, constr(strip_whitespace=True, min_length=1)]
    error: Annotated[str, constr(strip_whitespace=True, min_length=1)]
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class BaseRequestCommand(BaseModel):
    pass
