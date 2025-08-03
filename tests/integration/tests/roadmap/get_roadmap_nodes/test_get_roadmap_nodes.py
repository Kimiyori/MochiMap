from uuid import UUID, uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.modules.roadmap.domain.node.node import Node


class TestGetRoadmapNodesSuccess:
    """Test successful scenarios for getting roadmap nodes."""

    @pytest.mark.parametrize("num_nodes", [4])
    async def test_get_nodes_from_roadmap_with_multiple_nodes(
        self, client: AsyncClient, created_nodes: tuple[UUID, list[Node]]
    ) -> None:
        roadmap_id,existed_nodes = created_nodes

        response = await client.get(f"/roadmap/{roadmap_id}/nodes")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == len(existed_nodes)

        assert all(
            node["id"] in [str(n.id) for n in existed_nodes] for node in response_data
        ), "All nodes should be present in the response"



    @pytest.mark.parametrize("num_nodes", [0])
    async def test_get_nodes_from_empty_roadmap(
        self,
        client: AsyncClient,
        created_nodes: tuple[UUID, list[Node]]
    ) -> None:
        roadmap_id, existed_nodes = created_nodes

        response = await client.get(f"/roadmap/{roadmap_id}/nodes")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == len(existed_nodes)



class TestGetRoadmapNodesError:

    async def test_get_nodes_non_existent_roadmap(
        self,
        client: AsyncClient,
    ) -> None:
        response = await client.get(f"/roadmap/{uuid4()}/nodes")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 0, "Response should be an empty list for non-existent roadmap"

    async def test_get_nodes_invalid_roadmap_id(
        self,
        client: AsyncClient,
    ) -> None:

        response = await client.get(f"/roadmap/{'invalid_uuid'}/nodes")

        assert response.status_code == status.HTTP_404_NOT_FOUND


