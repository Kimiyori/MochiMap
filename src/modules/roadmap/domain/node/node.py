from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal
from uuid import UUID, uuid4

from src.modules.roadmap.domain.node.errors import UnknownNodeTypeError
from src.modules.roadmap.domain.node.value_objects import LearningNodeData, NodeType, Position, ResourceNodeData
from src.modules.roadmap.use_cases.create_new_node.command import CreateLearningNote, CreateResourceBookmark

if TYPE_CHECKING:
    from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand
    from src.modules.roadmap.use_cases.move_node.command import MoveNodeCommand

NodeData = LearningNodeData | ResourceNodeData


@dataclass()
class Node:
    id: UUID
    type: NodeType
    position: Position
    roadmap_id: UUID
    data: NodeData

    @staticmethod
    def new_node(roadmap_id: UUID, command: "CreateNodeCommand") -> "Node":
        new_id = uuid4()
        node_data = Node.setup_data(command.type, command.data)

        return Node(
            id=new_id,
            type=command.type,
            position=Position(x=command.position.x, y=command.position.y),
            roadmap_id=roadmap_id,
            data=node_data,
        )

    @staticmethod
    def setup_data(
        type: Literal[NodeType.LEARNING_NOTE, NodeType.RESOURCE_BOOKMARK],
        data: CreateLearningNote | CreateResourceBookmark,
    ) -> NodeData:
        if not data:
            raise ValueError("Data must be provided to create a node.")
        match type:
            case NodeType.LEARNING_NOTE:
                node_data = LearningNodeData(**data.model_dump())
            case NodeType.RESOURCE_BOOKMARK:
                node_data = ResourceNodeData(**data.model_dump())
            case _:
                raise UnknownNodeTypeError(type)
        return node_data

    def move_node(self, command: "MoveNodeCommand") -> None:
        if not command.position:
            raise ValueError("Position must be provided to move the node.")
        self.position = Position(x=command.position.x, y=command.position.y)
