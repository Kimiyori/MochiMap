from typing import Any
from uuid import UUID

import pytest
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.models.base_model import Base
from src.modules.roadmap.domain.edge.edge import Edge
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.node.value_objects import NodeType
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap
from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand, PositionDTO
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


@pytest.fixture
def num_roadmaps() -> int:
    return 1


@pytest.fixture
def num_edges() -> int:
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
async def check_if_exists(session: AsyncSession, model: Base):
    async def _check_if_exists() -> bool:
        await session.flush()
        result = await session.execute(select(model))
        data = result.scalar_one_or_none()
        assert data is not None

    yield
    await _check_if_exists()

@pytest.fixture
async def check_if_not_exists(session: AsyncSession, model: Base):
    async def _check_if_not_exists() -> bool:
        await session.flush()
        result = await session.execute(select(model))
        data = result.scalar_one_or_none()
        assert data is None

    yield
    await _check_if_not_exists()

@pytest.fixture
def created_roadmaps(session, num_roadmaps: int) -> list[Roadmap]:
    roadmaps: list[Roadmap] = []
    for i in range(num_roadmaps):
        command = CreateRoadmapCommand(
            title=f"Test Roadmap {i + 1}", description=f"Test description for roadmap {i + 1}"
        )
        roadmap = Roadmap.new_roadmap(command)
        session.add(roadmap)
        roadmaps.append(roadmap)
    return roadmaps


@pytest.fixture
async def created_nodes(
    faker: Faker,
    session: AsyncSession,
    created_roadmaps: list[Roadmap],
    generate_node_data_based_on_type,
    num_nodes: int,
) -> tuple[UUID, list[Node]]:
    roadmap_id = created_roadmaps[0].id
    nodes: list[Node] = []
    for _ in range(num_nodes):
        node_type: NodeType = faker.random_element([NodeType.LEARNING_NOTE, NodeType.RESOURCE_BOOKMARK])
        data = CreateNodeCommand(
            type=node_type,
            position=PositionDTO(
                x=faker.random_int(min=0, max=100),
                y=faker.random_int(min=0, max=100),
            ),
            data=generate_node_data_based_on_type(node_type),
        )
        new_node = Node.new_node(roadmap_id=roadmap_id, command=data)
        nodes.append(new_node)
    session.add_all(nodes)
    await session.flush()
    return roadmap_id, nodes


@pytest.fixture
async def created_edges(
    session: AsyncSession,
    created_nodes: tuple[UUID, list[Node]],
    num_edges: int,
) -> list[Edge]:
    roadmap_id, nodes = created_nodes
    edges: list[Edge] = []
    assert len(nodes) >= 2
    for i in range(num_edges):
        edge = Edge.new_edge(
            roadmap_id=roadmap_id,
            source_id=nodes[i].id,
            target_id=nodes[i + 1].id,
        )
        edges.append(edge)
    session.add_all(edges)
    await session.flush()
    return edges
