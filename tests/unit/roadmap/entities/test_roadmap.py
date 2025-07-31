from uuid import UUID

from src.modules.roadmap.domain.node.value_objects import NodeType
from src.modules.roadmap.domain.roadmap import Roadmap
from src.modules.roadmap.use_cases.create_new_node.command import (
    CreateNodeCommand,
    CreateResourceBookmark,
)
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


def test_new_roadmap_creates_roadmap_with_expected_fields():
    cmd = CreateRoadmapCommand(title="Learn Python", description="Python basics")
    roadmap = Roadmap.new_roadmap(cmd)
    assert isinstance(roadmap, Roadmap)
    assert roadmap.title == "Learn Python"
    assert roadmap.description == "Python basics"
    assert isinstance(roadmap.id, UUID)
    assert roadmap.nodes == []


def test_create_node_adds_node_to_roadmap():
    roadmap = Roadmap.new_roadmap(CreateRoadmapCommand(title="Learn Python", description="Python basics"))

    cmd = CreateNodeCommand.model_construct(
        title="Test Node",
        type=NodeType.RESOURCE_BOOKMARK,
        data=CreateResourceBookmark.model_construct(url="Test content", title="Test Learning Note"),
        position_x=0.0,
        position_y=0.0,
    )
    node = roadmap.create_node(cmd)
    assert roadmap.nodes == [node]
