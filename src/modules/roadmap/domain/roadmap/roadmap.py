from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.modules.roadmap.domain.edge.edge import Edge
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.roadmap.errors import RoadmapValidationError
from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


@dataclass()
class Roadmap:
    id: UUID
    title: str
    description: str | None = ""
    nodes: list[Node] | None = field(default_factory=list)
    edges: list[Edge] | None = field(default_factory=list)

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        invalid_fields = []
        if not self.title or not self.title.strip():
            invalid_fields.append("title")
        if invalid_fields:
            raise RoadmapValidationError(invalid_fields)

    @staticmethod
    def new_roadmap(command: CreateRoadmapCommand) -> "Roadmap":
        new_id = uuid4()
        return Roadmap(
            id=new_id,
            title=command.title,
            description=command.description,
        )

    def create_node(self, command: CreateNodeCommand):
        node = Node.new_node(self.id, command)
        self.nodes.append(node)
        return node

    def create_edge(self, source_id: UUID, target_id: UUID) -> Edge:
        edge = Edge.new_edge(self.id, source_id, target_id)
        self.edges.append(edge)
        return edge
