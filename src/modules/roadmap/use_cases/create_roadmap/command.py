from uuid import UUID

from src.common.pydantic import BaseRequestCommand
from src.modules.roadmap.domain.value_objects import Difficulty, EstimatedTime


class CreateRoadmapCommand(BaseRequestCommand):
    title: str
    description: str | None
    owner_id: UUID
    difficulty: Difficulty
    estimated_time: EstimatedTime
