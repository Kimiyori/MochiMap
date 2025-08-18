from uuid import UUID, uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.modules.roadmap.domain.node.node import Node


class TestGetRoadmapNodesSuccess:
    """Test successful scenarios for getting roadmap nodes."""

    async def make_request(self, client: AsyncClient, roadmap_id: UUID) -> object:
        return await client.get(f"/roadmap/{roadmap_id}/data")

    @pytest.mark.parametrize("num_nodes", [4])
    async def test_get_nodes_from_roadmap_with_multiple_nodes(
        self, client: AsyncClient, created_nodes: tuple[UUID, list[Node]]
    ) -> None:
        roadmap_id, existed_nodes = created_nodes

        response = await self.make_request(client, roadmap_id)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "nodes" in response_data
        assert "edges" in response_data

        nodes = response_data["nodes"]
        edges = response_data["edges"]
        assert isinstance(nodes, list)
        assert isinstance(edges, list)
        assert len(nodes) == len(existed_nodes)
        assert len(edges) == 0

        assert all(node["id"] in [str(n.id) for n in existed_nodes] for node in nodes), (
            "All nodes should be present in the response"
        )

    @pytest.mark.parametrize("num_nodes", [0])
    async def test_get_nodes_from_empty_roadmap(
        self,
        client: AsyncClient,
        created_nodes: tuple[UUID, list[Node]],
    ) -> None:
        roadmap_id, existed_nodes = created_nodes

        response = await self.make_request(client, roadmap_id)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "nodes" in response_data and isinstance(response_data["nodes"], list)
        assert "edges" in response_data and isinstance(response_data["edges"], list)
        assert len(response_data["nodes"]) == len(existed_nodes)
        assert len(response_data["edges"]) == 0

    @pytest.mark.parametrize("num_nodes", [2])
    @pytest.mark.parametrize("num_edges", [1])
    async def test_get_roadmap_data_with_edges(
        self,
        client: AsyncClient,
        created_nodes: tuple[UUID, list[Node]],
        created_edges: list,
        num_edges: int,
    ) -> None:
        # consume param to satisfy linter
        assert num_edges == 1
        assert len(created_edges) == 1
        roadmap_id, nodes = created_nodes

        response = await self.make_request(client, roadmap_id)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, dict)
        assert "edges" in data and isinstance(data["edges"], list)
        assert len(data["edges"]) == 1
        edge_payload = data["edges"][0]
        assert edge_payload["source"] == str(nodes[0].id)
        assert edge_payload["target"] == str(nodes[1].id)


class TestGetRoadmapNodesError:
    async def test_get_nodes_non_existent_roadmap(
        self,
        client: AsyncClient,
    ) -> None:
        r = await client.get(f"/roadmap/{uuid4()}/data")
        assert r.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_nodes_invalid_roadmap_id(
        self,
        client: AsyncClient,
    ) -> None:
        response = await client.get("/roadmap/invalid_uuid/data")
        assert response.status_code == status.HTTP_404_NOT_FOUND
