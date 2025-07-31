from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


@dataclass()
class Roadmap:
    id: UUID
    title: str
    description: str
    nodes: list[Node] | None = field(default_factory=list)

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
