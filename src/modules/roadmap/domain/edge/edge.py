from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from src.modules.roadmap.domain.edge.errors import SelfLoopEdgeError


@dataclass()
class Edge:
    id: UUID
    roadmap_id: UUID
    source_id: UUID
    target_id: UUID

    @staticmethod
    def new_edge(roadmap_id: UUID, source_id: UUID, target_id: UUID) -> Edge:
        if source_id == target_id:
            raise SelfLoopEdgeError()
        return Edge(id=uuid4(), roadmap_id=roadmap_id, source_id=source_id, target_id=target_id)
