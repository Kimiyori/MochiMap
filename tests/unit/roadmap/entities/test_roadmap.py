from typing import TYPE_CHECKING
from uuid import UUID

import pytest

from src.modules.roadmap.domain.node.value_objects import NodeType
from src.modules.roadmap.domain.roadmap.errors import RoadmapValidationError
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap

if TYPE_CHECKING:
    from faker import Faker

    from tests.unit.roadmap.conftest import NodeTestDataFactory, RoadmapTestDataFactory


class TestRoadmapCreation:
    def test_new_roadmap_creates_roadmap_with_expected_fields(
        self,
        roadmap_factory: "RoadmapTestDataFactory",
        fake: "Faker",
    ):
        title = fake.sentence(nb_words=4)
        description = fake.text(max_nb_chars=200)

        roadmap = roadmap_factory.create_roadmap(title=title, description=description)

        assert isinstance(roadmap, Roadmap)
        assert roadmap.title == title
        assert roadmap.description == description
        assert isinstance(roadmap.id, UUID)
        assert roadmap.nodes == []

    def test_new_roadmap_with_minimal_data(
        self,
        roadmap_factory: "RoadmapTestDataFactory",
        fake: "Faker",
    ):
        title = fake.word()
        roadmap = roadmap_factory.create_roadmap(title=title, description="")

        assert roadmap.title == title
        assert roadmap.description == ""
        assert roadmap.nodes == []


class TestRoadmapNodeManagement:
    def test_create_node_adds_learning_note_to_roadmap(
        self,
        roadmap_factory: "RoadmapTestDataFactory",
        node_factory: "NodeTestDataFactory",
        fake: "Faker",
    ):
        roadmap = roadmap_factory.create_roadmap()

        title = fake.sentence(nb_words=3)
        content = fake.text(max_nb_chars=100)
        cmd = node_factory.create_node_command(node_type=NodeType.LEARNING_NOTE, title=title, content=content)

        node = roadmap.create_node(cmd)

        assert len(roadmap.nodes) == 1
        assert roadmap.nodes[0] == node
        assert node.roadmap_id == roadmap.id
        assert node.type == NodeType.LEARNING_NOTE
        assert node.data.title == title
        assert node.data.content == content

    def test_create_node_adds_resource_bookmark_to_roadmap(
        self,
        roadmap_factory: "RoadmapTestDataFactory",
        node_factory: "NodeTestDataFactory",
        fake: "Faker",
    ):
        roadmap = roadmap_factory.create_roadmap()

        title = fake.sentence(nb_words=3)
        url = fake.url()
        cmd = node_factory.create_node_command(node_type=NodeType.RESOURCE_BOOKMARK, title=title, url=url)

        node = roadmap.create_node(cmd)

        assert len(roadmap.nodes) == 1
        assert roadmap.nodes[0] == node
        assert node.roadmap_id == roadmap.id
        assert node.type == NodeType.RESOURCE_BOOKMARK
        assert node.data.title == title
        assert node.data.url == url

    def test_create_multiple_nodes_in_roadmap(
        self,
        roadmap_factory: "RoadmapTestDataFactory",
        node_factory: "NodeTestDataFactory",
        fake: "Faker",
    ):
        roadmap = roadmap_factory.create_roadmap()

        learning_cmd = node_factory.create_node_command(
            node_type=NodeType.LEARNING_NOTE, title=fake.sentence(nb_words=3)
        )
        resource_cmd = node_factory.create_node_command(
            node_type=NodeType.RESOURCE_BOOKMARK, title=fake.sentence(nb_words=3)
        )
        learning_cmd2 = node_factory.create_node_command(
            node_type=NodeType.LEARNING_NOTE, title=fake.sentence(nb_words=3)
        )

        node1 = roadmap.create_node(learning_cmd)
        node2 = roadmap.create_node(resource_cmd)
        node3 = roadmap.create_node(learning_cmd2)

        assert len(roadmap.nodes) == 3
        assert roadmap.nodes == [node1, node2, node3]

        for node in roadmap.nodes:
            assert node.roadmap_id == roadmap.id


class TestRoadmapBoundaryValues:
    def test_roadmap_with_empty_title(
        self,
        roadmap_factory: "RoadmapTestDataFactory",
    ):
        with pytest.raises(RoadmapValidationError, match="Title must not be empty."):
            roadmap_factory.create_roadmap(title="", description="")
