from typing import Literal

from pydantic import Field, model_validator

from src.common.pydantic import BaseRequestCommand
from src.modules.roadmap.domain.node.value_objects import NodeType


class BaseNodeCommand(BaseRequestCommand):
    title: str


class CreateLearningNote(BaseNodeCommand):
    content: str = ""


class CreateResourceBookmark(BaseNodeCommand):
    url: str


class CreateNodeCommand(BaseRequestCommand):
    type: Literal[NodeType.LEARNING_NOTE, NodeType.RESOURCE_BOOKMARK] = Field(..., description="Type of node")
    data: CreateLearningNote | CreateResourceBookmark

    position_x: float
    position_y: float

    @model_validator(mode="before")
    def validate_data(self, values):
        node_type = values.get("type")
        data = values.get("data")
        if node_type == NodeType.LEARNING_NOTE:
            values["data"] = CreateLearningNote(**(data or {}))
        elif node_type == NodeType.RESOURCE_BOOKMARK:
            values["data"] = CreateResourceBookmark(**(data or {}))
        return values
