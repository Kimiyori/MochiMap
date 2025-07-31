from abc import ABC
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from src.modules.roadmap.domain.node.value_objects import NodeType, Position


class BaseNodeDataResponseDTO(BaseModel, ABC):
    title: str

class LearningNodeDataResponseDTO(BaseNodeDataResponseDTO):
    """Response DTO for learning node data"""

    content: str | None = None


class ResourceNodeDataResponseDTO(BaseNodeDataResponseDTO):
    """Response DTO for resource node data"""

    url: str = ""


class BaseNodeResponseDTO(BaseModel, ABC):
    """Base response DTO for all node types"""

    id: UUID
    position: Position


class LearningNodeResponseDTO(BaseNodeResponseDTO):
    """Response DTO for learning note nodes"""

    type: Literal[NodeType.LEARNING_NOTE] = NodeType.LEARNING_NOTE
    data: LearningNodeDataResponseDTO


class ResourceNodeResponseDTO(BaseNodeResponseDTO):
    """Response DTO for resource bookmark nodes"""

    type: Literal[NodeType.RESOURCE_BOOKMARK] = NodeType.RESOURCE_BOOKMARK
    data: ResourceNodeDataResponseDTO


# Discriminated union for different node types
GetRoadmapNodesResponseDTO = Annotated[LearningNodeResponseDTO | ResourceNodeResponseDTO, Field(discriminator="type")]
