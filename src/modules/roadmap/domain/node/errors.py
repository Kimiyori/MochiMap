from src.modules.roadmap.domain.node.value_objects import NodeType


class UnknownNodeTypeError(ValueError):
    def __init__(self, node_type: NodeType) -> None:
        super().__init__(f"Unknown node type: {node_type}")
