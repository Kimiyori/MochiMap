import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.models.edges.edges import EdgeModel


class TestDeleteEdge:
    @pytest.mark.parametrize("num_edges,num_nodes", [(1, 2)])
    async def test_delete_edge_success(
        self,
        client: AsyncClient,
        created_edges: list,
        session: AsyncSession,
    ) -> None:
        edge = created_edges[0]

        response = await client.delete(f"/roadmap/edge/{edge.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        result = await session.execute(select(EdgeModel))
        edges = result.scalars().all()
        assert len(edges) == 0

    async def test_delete_edge_not_found(self, client: AsyncClient) -> None:
        import uuid

        non_existent_edge_id = uuid.uuid4()
        response = await client.delete(f"/roadmap/edge/{non_existent_edge_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
