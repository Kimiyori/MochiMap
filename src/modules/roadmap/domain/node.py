from dataclasses import dataclass
from uuid import UUID

from src.modules.roadmap.domain.value_objects import Difficulty, EstimatedTime, NodeType, Position, Resource, TimeUnit


@dataclass
class Node:
    id: UUID
    title: str
    description: str
    node_type: NodeType
    difficulty: Difficulty
    estimated_time: EstimatedTime
    estimated_time_unit: TimeUnit
    position: Position
    resources: list[Resource]

    def add_resource(self, resource: Resource) -> None:
        self.resources.append(resource)

    def add_prerequisite(self, node_id: UUID) -> None:
        if node_id not in self.prerequisites:
            self.prerequisites.append(node_id)

    def add_next_node(self, node_id: UUID) -> None:
        if node_id not in self.next_nodes:
            self.next_nodes.append(node_id)
