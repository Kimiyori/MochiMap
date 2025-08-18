from uuid import uuid4

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from src.modules.roadmap.domain.node.node import Node


class TestMoveNodeUseCase:
    @pytest.mark.parametrize("num_nodes", [1])
    async def test_move_success(
        self,
        faker: Faker,
        client: AsyncClient,
        created_nodes: tuple[str, Node],
    ) -> None:
        _, node = created_nodes

        update_data = {
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=200),
                "y": faker.pyfloat(min_value=0, max_value=200),
            },
        }
        response = await client.put(f"/roadmap/node/{node.id!s}/move", json=update_data)
        assert response.status_code == status.HTTP_200_OK



class TestMoveNodeErrorUseCase:
    async def test_update_non_existent_node_fails(self, faker: Faker, client: AsyncClient) -> None:
        non_existent_node_id = uuid4()
        update_data = {
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=100),
                "y": faker.pyfloat(min_value=0, max_value=100),
            },
        }

        response = await client.put(f"/roadmap/node/{non_existent_node_id}/move", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_node_invalid_node_id_fails(self, faker: Faker, client: AsyncClient) -> None:
        invalid_node_id = "invalid_uuid"
        update_data = {
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=100),
                "y": faker.pyfloat(min_value=0, max_value=100),
            },
        }

        response = await client.put(f"/roadmap/node/{invalid_node_id}/move", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND