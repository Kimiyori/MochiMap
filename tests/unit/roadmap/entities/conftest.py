from uuid import UUID, uuid4

import pytest
from faker import Faker

from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.node.value_objects import NodeType
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap
from src.modules.roadmap.use_cases.create_new_node.command import (
    CreateLearningNote,
    CreateNodeCommand,
    CreateResourceBookmark,
    PositionDTO,
)
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


class NodeTestDataFactory:
    def __init__(self, fake: Faker):
        self.fake = fake

    def create_learning_note_data(self, title: str | None = None, content: str | None = None) -> CreateLearningNote:
        return CreateLearningNote.model_construct(
            title=title if title is not None else self.fake.sentence(nb_words=4).rstrip("."),
            content=content if content is not None else self.fake.text(max_nb_chars=200),
        )

    def create_resource_bookmark_data(self, title: str | None = None, url: str | None = None) -> CreateResourceBookmark:
        return CreateResourceBookmark.model_construct(
            title=title if title is not None else self.fake.sentence(nb_words=3).rstrip("."),
            url=url if url is not None else self.fake.url(),
        )

    def create_node_command(
        self,
        node_type: NodeType | None = None,
        title: str | None = None,
        position_x: float | None = None,
        position_y: float | None = None,
        **data_kwargs,
    ) -> CreateNodeCommand:
        node_type = node_type or self.fake.random_element(elements=[NodeType.LEARNING_NOTE, NodeType.RESOURCE_BOOKMARK])

        if node_type == NodeType.LEARNING_NOTE:
            data = self.create_learning_note_data(title=title, content=data_kwargs.get("content"))
        elif node_type == NodeType.RESOURCE_BOOKMARK:
            data = self.create_resource_bookmark_data(title=title, url=data_kwargs.get("url"))

        position = PositionDTO(
            x=position_x if position_x is not None else self.fake.pyfloat(min_value=-100, max_value=100),
            y=position_y if position_y is not None else self.fake.pyfloat(min_value=-100, max_value=100),
        )

        return CreateNodeCommand.model_construct(
            type=node_type,
            data=data,
            position=position,
        )

    def create_invalid_node_command(self, invalid_type: str = "INVALID_TYPE") -> CreateNodeCommand:
        position = PositionDTO(
            x=self.fake.pyfloat(min_value=-100, max_value=100),
            y=self.fake.pyfloat(min_value=-100, max_value=100),
        )
        return CreateNodeCommand.model_construct(
            type=invalid_type,
            data=self.create_learning_note_data(),
            position=position,
        )

    def create_node(
        self,
        roadmap_id: UUID,
        node_type: NodeType | None = None,
        title: str | None = None,
        position_x: float | None = None,
        position_y: float | None = None,
        **data_kwargs,
    ) -> Node:
        cmd = self.create_node_command(
            node_type=node_type,
            title=title,
            position_x=position_x,
            position_y=position_y,
            **data_kwargs,
        )
        return Node.new_node(roadmap_id, cmd)

class RoadmapTestDataFactory:
    def __init__(self, fake: Faker):
        self.fake = fake

    def create_roadmap_command(self, title: str | None = None, description: str | None = None) -> CreateRoadmapCommand:
        return CreateRoadmapCommand(
            title=title if title is not None else self.fake.sentence(nb_words=3).rstrip("."),
            description=description if description is not None else self.fake.text(max_nb_chars=100),
        )

    def create_roadmap(self, title: str | None = None, description: str | None = None) -> Roadmap:
        cmd = self.create_roadmap_command(title, description)
        return Roadmap.new_roadmap(cmd)


@pytest.fixture
def node_factory(fake: Faker) -> NodeTestDataFactory:
    return NodeTestDataFactory(fake)


@pytest.fixture
def learning_note_node(roadmap_id: UUID, node_factory: NodeTestDataFactory) -> Node:
    return node_factory.create_node(
        roadmap_id=roadmap_id,
        node_type=NodeType.LEARNING_NOTE,
    )


@pytest.fixture
def resource_bookmark_node(roadmap_id: UUID, node_factory: NodeTestDataFactory) -> Node:
    return node_factory.create_node(
        roadmap_id=roadmap_id,
        node_type=NodeType.RESOURCE_BOOKMARK,
    )


@pytest.fixture
def roadmap_factory(fake: Faker) -> RoadmapTestDataFactory:
    return RoadmapTestDataFactory(fake)


@pytest.fixture
def created_roadmap(roadmap_factory: RoadmapTestDataFactory) -> Roadmap:
    return roadmap_factory.create_roadmap()


@pytest.fixture
def roadmap_id() -> UUID:
    return uuid4()
