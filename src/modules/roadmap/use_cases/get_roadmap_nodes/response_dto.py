from abc import ABC
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

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
