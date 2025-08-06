from typing import TYPE_CHECKING
from uuid import UUID

import pytest

from src.modules.roadmap.domain.node.errors import UnknownNodeTypeError
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.node.value_objects import NodeType

if TYPE_CHECKING:
    from uuid import UUID

    from tests.unit.roadmap.entities.conftest import NodeTestDataFactory


class TestNodeCreation:
    def test_new_node_creates_learning_note_node(
        self,
        learning_note_node: Node,
        roadmap_id: "UUID",
    ):
        node = learning_note_node

        assert isinstance(node, Node)
        assert node.type == NodeType.LEARNING_NOTE
        assert node.roadmap_id == roadmap_id
        assert isinstance(node.data.content, str)
        assert isinstance(node.data.title, str)
        assert isinstance(node.id, UUID)
        assert node.id != roadmap_id

    def test_new_node_creates_resource_bookmark_node(
        self,
        resource_bookmark_node: Node,
        roadmap_id: "UUID",
    ):
        node = resource_bookmark_node

        assert isinstance(node, Node)
        assert node.type == NodeType.RESOURCE_BOOKMARK
        assert node.roadmap_id == roadmap_id
        assert isinstance(node.data.url, str)
        assert isinstance(node.data.title, str)
        assert isinstance(node.id, UUID)

    def test_new_node_raises_on_unknown_type(
        self,
        roadmap_id: "UUID",
        node_factory: "NodeTestDataFactory",
    ):
        cmd = node_factory.create_invalid_node_command(invalid_type="UNKNOWN_TYPE")

        with pytest.raises(UnknownNodeTypeError) as exc_info:
            Node.new_node(roadmap_id, cmd)

        assert "Unknown node type: UNKNOWN_TYPE" in str(exc_info.value)
