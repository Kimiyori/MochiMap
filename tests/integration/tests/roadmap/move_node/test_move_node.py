from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.modules.roadmap.domain.node.node import Node


class TestMoveNodeUseCase:
    @pytest.mark.parametrize("num_nodes", [1])
    async def test_move_success(
        self, client: AsyncClient, created_nodes: tuple[str, Node], random_position: dict[str, float]
    ) -> None:
        _, node = created_nodes

        move_data = {"position": random_position}
        response = await client.put(f"/roadmap/node/{node.id!s}/move", json=move_data)
        assert response.status_code == status.HTTP_200_OK



class TestMoveNodeErrorUseCase:
    async def test_move_non_existent_node_fails(self,  client: AsyncClient, random_position: dict[str, float]) -> None:
        non_existent_node_id = uuid4()
        update_data = {
            "position": random_position,
        }

        response = await client.put(f"/roadmap/node/{non_existent_node_id}/move", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_move_node_invalid_node_id_fails(self, client: AsyncClient, random_position: dict[str, float]) -> None:
        invalid_node_id = "invalid_uuid"
        update_data = {"position": random_position}

        response = await client.put(f"/roadmap/node/{invalid_node_id}/move", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND