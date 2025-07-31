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
class LearningNodeData:
    title: str
    content: str | None = None


@dataclass(frozen=True)
class ResourceNodeData:
    title: str
    url: str = ""
