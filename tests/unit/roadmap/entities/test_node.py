from typing import TYPE_CHECKING
from uuid import UUID

import pytest

from src.modules.roadmap.domain.node.errors import UnknownNodeTypeError
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.node.value_objects import NodeType, Position

if TYPE_CHECKING:
    from uuid import UUID

    from tests.unit.roadmap.conftest import NodeTestDataFactory


class TestNodeCreation:
    def test_new_node_creates_learning_note_node(
        self,
        roadmap_id: "UUID",
        node_factory: "NodeTestDataFactory",
    ):
        cmd = node_factory.create_node_command(
            node_type=NodeType.LEARNING_NOTE,
            title="Learning Note Node",
            content="Some content",
            position_x=1.5,
            position_y=2.5,
        )

        node = Node.new_node(roadmap_id, cmd)

        assert isinstance(node, Node)
        assert node.type == NodeType.LEARNING_NOTE
        assert node.position == Position(x=1.5, y=2.5)
        assert node.roadmap_id == roadmap_id
        assert node.data.content == "Some content"
        assert node.data.title == "Learning Note Node"
        assert isinstance(node.id, UUID)
        assert node.id != roadmap_id  # Ensure new ID is generated

    def test_new_node_creates_resource_bookmark_node(
        self,
        roadmap_id: "UUID",
        node_factory: "NodeTestDataFactory",
    ):
        cmd = node_factory.create_node_command(
            node_type=NodeType.RESOURCE_BOOKMARK,
            title="Resource Node",
            url="https://example.com",
            position_x=0.0,
            position_y=0.0,
        )

        node = Node.new_node(roadmap_id, cmd)

        assert isinstance(node, Node)
        assert node.type == NodeType.RESOURCE_BOOKMARK
        assert node.position == Position(x=0.0, y=0.0)
        assert node.roadmap_id == roadmap_id
        assert node.data.url == "https://example.com"
        assert node.data.title == "Resource Node"
        assert isinstance(node.id, UUID)
        assert node.id != roadmap_id  # Ensure new ID is generated

    def test_new_node_generates_unique_ids(
        self,
        roadmap_id: "UUID",
        node_factory: "NodeTestDataFactory",
    ):
        cmd1 = node_factory.create_node_command(node_type=NodeType.LEARNING_NOTE)
        cmd2 = node_factory.create_node_command(node_type=NodeType.RESOURCE_BOOKMARK)

        node1 = Node.new_node(roadmap_id, cmd1)
        node2 = Node.new_node(roadmap_id, cmd2)

        assert node1.id != node2.id
        assert node1.id != roadmap_id
        assert node2.id != roadmap_id


class TestNodeValidation:
    def test_new_node_raises_on_unknown_type(
        self,
        roadmap_id: "UUID",
        node_factory: "NodeTestDataFactory",
    ):
        cmd = node_factory.create_invalid_node_command(invalid_type="UNKNOWN_TYPE")

        with pytest.raises(UnknownNodeTypeError) as exc_info:
            Node.new_node(roadmap_id, cmd)

        assert "Unknown node type: UNKNOWN_TYPE" in str(exc_info.value)
