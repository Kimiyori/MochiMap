
from pydantic import BaseModel

from src.common.pydantic import BaseRequestCommand


class PositionDTO(BaseModel):
    x: float
    y: float


class MoveNodeCommand(BaseRequestCommand):

    position: PositionDTO | None = None
