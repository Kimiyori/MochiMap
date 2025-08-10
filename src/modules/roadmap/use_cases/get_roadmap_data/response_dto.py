from abc import ABC
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.modules.roadmap.domain.node.value_objects import NodeType


class BaseNodeDataResponseDTO(BaseModel, ABC):
    title: str


class LearningNodeDataResponseDTO(BaseNodeDataResponseDTO):
    """Response DTO for learning node data"""

    content: str | None = None


class ResourceNodeDataResponseDTO(BaseNodeDataResponseDTO):
    """Response DTO for resource node data"""

    url: str = ""


class PositionDTO(BaseModel):
    x: float
    y: float


class GetRoadmapNodesResponseDTO(BaseModel):
    id:UUID
    type: Literal[NodeType.LEARNING_NOTE, NodeType.RESOURCE_BOOKMARK] = Field(..., description="Type of node")
    data: LearningNodeDataResponseDTO | ResourceNodeDataResponseDTO
    position: PositionDTO

class GetRoadmapEdgesResponseDTO(BaseModel):
    id: UUID
    source: UUID
    target: UUID

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def map_aliases(cls, values: dict) -> dict:
        data = dict(values.__dict__)
        if "source_id" in data and "source" not in data:
            data["source"] = data["source_id"]
        if "target_id" in data and "target" not in data:
            data["target"] = data["target_id"]
        return data

class GetRoadmapDataResponseDTO(BaseModel):
    nodes: list[GetRoadmapNodesResponseDTO]= Field(default_factory=list)
    edges: list[GetRoadmapEdgesResponseDTO]= Field(default_factory=list)

