import uuid

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.models.edges.edges import EdgeModel
from src.infrastructure.persistence.models.node.node import NodeModel


async def make_delete_request(client: AsyncClient, node_id: uuid.UUID):
    return await client.delete(f"/roadmap/node/{node_id}")


class TestDeleteNode:
    @pytest.mark.parametrize("num_nodes", [2])
    async def test_delete_node_success(
        self,
        client: AsyncClient,
        created_nodes: tuple[str, list],
        session: AsyncSession,
    ) -> None:
        _, nodes = created_nodes
        node_to_delete = nodes[0]
        response = await make_delete_request(client, node_to_delete.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        remaining_nodes = (await session.execute(select(NodeModel))).scalars().all()
        assert all(str(n.id) != str(node_to_delete.id) for n in remaining_nodes)
        assert len(remaining_nodes) == len(nodes) - 1

    async def test_delete_node_not_found(self, client: AsyncClient) -> None:
        non_existent_node_id = uuid.uuid4()
        response = await make_delete_request(client, non_existent_node_id)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize("num_nodes", [3])
    @pytest.mark.parametrize("num_edges", [2])
    @pytest.mark.usefixtures("created_edges")
    async def test_delete_node_cascade_edges(
        self,
        client: AsyncClient,
        created_nodes: tuple[str, list],
        session: AsyncSession,
    ) -> None:
        _, nodes = created_nodes
        node_to_delete = nodes[1]
        response = await make_delete_request(client, node_to_delete.id)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        remaining_nodes = (await session.execute(select(NodeModel))).scalars().all()
        remaining_edges = (await session.execute(select(EdgeModel))).scalars().all()
        assert str(node_to_delete.id) not in {str(n.id) for n in remaining_nodes}
        assert len(remaining_nodes) == 2
        assert len(remaining_edges) == 0
