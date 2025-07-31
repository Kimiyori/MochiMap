from uuid import UUID, uuid4

import pytest

from src.modules.roadmap.domain.node.errors import UnknownNodeTypeError
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.node.value_objects import NodeType, Position
from src.modules.roadmap.use_cases.create_new_node.command import (
    CreateNodeCommand,
    CreateLearningNote,
    CreateResourceBookmark,
)


def test_new_node_creates_learning_note_node():
    roadmap_id = uuid4()
    cmd = CreateNodeCommand.model_construct(
        title="Learning Note Node",
        type=NodeType.LEARNING_NOTE,
        data=CreateLearningNote.model_construct(content="Some content", title="Learning Note Node"),
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


def test_new_node_creates_resource_bookmark_node():
    roadmap_id = uuid4()
    cmd = CreateNodeCommand.model_construct(
        title="Resource Node",
        type=NodeType.RESOURCE_BOOKMARK,
        data=CreateResourceBookmark.model_construct(url="https://example.com", title="Resource Node"),
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

def test_new_node_raises_on_unknown_type():
    roadmap_id = uuid4()
    cmd = CreateNodeCommand.model_construct(
        title="Unknown Node",
        type="UNKNOWN_TYPE",
        data={},
        position_x=0.0,
        position_y=0.0,
    )
    with pytest.raises(UnknownNodeTypeError):
        Node.new_node(roadmap_id, cmd)