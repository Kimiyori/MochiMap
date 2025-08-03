
from src.common.pydantic import BaseRequestCommand


class CreateRoadmapCommand(BaseRequestCommand):
    title: str
    description: str | None = None

