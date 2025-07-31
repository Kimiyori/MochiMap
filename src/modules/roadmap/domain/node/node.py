from dataclasses import dataclass
from uuid import UUID, uuid4

from src.modules.roadmap.domain.node.errors import UnknownNodeTypeError
from src.modules.roadmap.domain.node.value_objects import LearningNodeData, NodeType, Position, ResourceNodeData
from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand


@dataclass()
class Node:
    id: UUID
    type: NodeType
    position: Position
    roadmap_id: UUID
    data: LearningNodeData | ResourceNodeData

    @staticmethod
    def new_node(roadmap_id: UUID, command: CreateNodeCommand) -> "Node":
        new_id = uuid4()

        match command.type:
            case NodeType.LEARNING_NOTE:
                node_data = LearningNodeData(**command.data.model_dump())
            case NodeType.RESOURCE_BOOKMARK:
                node_data = ResourceNodeData(**command.data.model_dump())
            case _:
                raise UnknownNodeTypeError(command.type)

        return Node(
            id=new_id,
            type=command.type,
            position=Position(x=command.position_x, y=command.position_y),
            roadmap_id=roadmap_id,
            data=node_data,
        )
