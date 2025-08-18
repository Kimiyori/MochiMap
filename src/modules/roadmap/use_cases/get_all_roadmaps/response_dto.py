from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RoadmapResponseDTO(BaseModel):
    id: UUID
    title: str
    description: str | None
    model_config = ConfigDict(from_attributes=True)
