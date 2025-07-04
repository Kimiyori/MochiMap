from uuid import UUID

from common.pydantic import BaseRequestCommand
from modules.roadmap.domain.value_objects import Difficulty, EstimatedTime, TimeUnit


class CreateRoadmapCommand(BaseRequestCommand):
    id: UUID
    title: str
    description: str | None
    owner_id: UUID
    difficulty: Difficulty
    estimated_time: EstimatedTime
    estimated_time_unit: TimeUnit
