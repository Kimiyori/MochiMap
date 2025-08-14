
from pydantic import BaseModel, model_validator

from src.common.pydantic import BaseRequestCommand
from src.modules.roadmap.domain.node.value_objects import NodeType


class PositionDTO(BaseModel):
    x: float
    y: float


class BaseNodeCommand(BaseRequestCommand):
    title: str


class CreateLearningNote(BaseNodeCommand):
    content: str | None = None


class CreateResourceBookmark(BaseNodeCommand):
    url: str


class CreateNodeCommand(BaseRequestCommand):
    type: NodeType
    data: CreateLearningNote | CreateResourceBookmark
    position: PositionDTO

    @model_validator(mode="before")
    @classmethod
    def validate_data(cls, values: dict) -> dict:
        node_type = values.get("type")
        data = values.get("data")
        if node_type == NodeType.LEARNING_NOTE:
            values["data"] = CreateLearningNote(**(data or {}))
        elif node_type == NodeType.RESOURCE_BOOKMARK:
            values["data"] = CreateResourceBookmark(**(data or {}))
        return values
