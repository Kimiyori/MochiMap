from uuid import UUID

from pydantic import BaseModel


class RoadmapResponseDTO(BaseModel):
    id: UUID
    title: str
    description: str | None
