from dataclasses import dataclass
from enum import Enum


class NodeType(str, Enum):
    LEARNING_NOTE = "LearningNote"
    RESOURCE_BOOKMARK = "ResourceBookmark"


@dataclass(frozen=True)
class Position:
    x: float
    y: float

@dataclass(frozen=True)
class BaseNodeData:
    title: str

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Title must not be empty.")

@dataclass(frozen=True)
class LearningNodeData(BaseNodeData):
    content: str | None = None


@dataclass(frozen=True)
class ResourceNodeData(BaseNodeData):
    url: str = ""
