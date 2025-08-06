from typing import Any

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.node.value_objects import NodeType
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap
from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand


@pytest.fixture
def num_roadmaps() -> int:
    return 1


@pytest.fixture
def num_nodes() -> int:
    return 2


@pytest.fixture
def generate_node_data_based_on_type(faker: Faker):
    def _generate_node_data(node_type: NodeType) -> Any:
        if node_type == NodeType.LEARNING_NOTE:
            return {"title": faker.sentence(), "content": faker.text()}
        if node_type == NodeType.RESOURCE_BOOKMARK:
            return {
                "title": faker.sentence(),
                "url": faker.url(),
            }
        return None

    return _generate_node_data


@pytest.fixture
def type() -> NodeType:
    return NodeType.LEARNING_NOTE


@pytest.fixture
async def created_nodes(
    faker: Faker,
    session: AsyncSession,
    created_roadmaps: list[Roadmap],
    generate_node_data_based_on_type,
    num_nodes: int,
    type: NodeType,
) -> tuple[str, list[Node] | Node]:
    roadmap_id = created_roadmaps[0].id
    nodes = []

    for _ in range(num_nodes):
        node_type = type

        data = CreateNodeCommand(
            type=node_type,
            position={"x": faker.pyfloat(min_value=0, max_value=100), "y": faker.pyfloat(min_value=0, max_value=100)},
            data=generate_node_data_based_on_type(node_type),
        )

        node = Node.new_node(roadmap_id, data)
        session.add(node)
        nodes.append(node)

    await session.flush()
    return str(roadmap_id), (nodes if num_nodes > 1 else nodes[0])
