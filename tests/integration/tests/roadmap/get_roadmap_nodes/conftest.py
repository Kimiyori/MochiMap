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
async def created_nodes(
    faker: Faker,
    session: AsyncSession,
    created_roadmaps: list[Roadmap],
    generate_node_data_based_on_type,
    num_nodes: int,
) -> dict[str, Any]:
    roadmap_id = created_roadmaps[0].id
    nodes = []
    for _ in range(num_nodes):
        node_type: NodeType = faker.random_element([NodeType.LEARNING_NOTE, NodeType.RESOURCE_BOOKMARK])

        data = CreateNodeCommand(
            type=node_type,
            position_x=faker.random_int(min=0, max=100),
            position_y=faker.random_int(min=0, max=100),
            data=generate_node_data_based_on_type(node_type),
        )
        new_node = Node.new_node(roadmap_id=roadmap_id, command=data)
        nodes.append(new_node)
    session.add_all(nodes)
    return roadmap_id, nodes
