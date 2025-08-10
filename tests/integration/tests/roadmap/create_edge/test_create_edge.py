from uuid import UUID, uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.infrastructure.persistence.models.edges.edges import EdgeModel


class TestCreateEdge:

    async def make_request(self, client: AsyncClient, roadmap_id: UUID, source_id: UUID, target_id: UUID):
        return await client.post(
            f"/roadmap/{roadmap_id}/edge", json={"source_id": str(source_id), "target_id": str(target_id)}
        )

    @pytest.mark.parametrize("model", [EdgeModel])
    async def test_create_edge_success(self, client: AsyncClient, created_nodes, check_if_exists):
        roadmap_id, nodes = created_nodes
        node1_id = nodes[0].id
        node2_id = nodes[1].id

        r = await self.make_request(client, roadmap_id, node1_id, node2_id)
        assert r.status_code == status.HTTP_201_CREATED
        assert await check_if_exists()

    async def test_create_edge_duplicate_same_pair_conflict(self, client: AsyncClient, created_nodes):
        roadmap_id, nodes = created_nodes
        node1_id = nodes[0].id
        node2_id = nodes[1].id

        ok = await self.make_request(client, roadmap_id, node1_id, node2_id)
        assert ok.status_code == status.HTTP_201_CREATED

        dup = await self.make_request(client, roadmap_id, node1_id, node2_id)
        assert dup.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.parametrize("num_nodes", [1])
    async def test_create_edge_missing_nodes_in_roadmap_fails(self, client: AsyncClient, created_nodes):
        roadmap_id, nodes = created_nodes
        other_roadmap_id = uuid4()

        bad = await self.make_request(client, roadmap_id, nodes[0].id, other_roadmap_id)
        assert bad.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize("num_nodes", [1])
    async def test_create_edge_self_loop_fails(self, client: AsyncClient, created_nodes):
        roadmap_id, nodes = created_nodes
        node_id = nodes[0].id

        r = await self.make_request(client, roadmap_id, node_id, node_id)
        assert r.status_code == status.HTTP_400_BAD_REQUEST
