from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


class SelfLoopEdgeError(ValueError):
    def __init__(self) -> None:
        super().__init__("Edge cannot connect a node to itself.")


@dataclass(frozen=True)
class NodeNotInRoadmapError(ValueError):
    missing_node_ids: tuple[UUID, ...]

    def __str__(self) -> str:
        return f"Node(s) not part of the roadmap: {', '.join(str(n) for n in self.missing_node_ids)}"


class DuplicateEdgeInRoadmapError(ValueError):
    def __init__(self) -> None:
        super().__init__("This edge already exists in the roadmap.")
