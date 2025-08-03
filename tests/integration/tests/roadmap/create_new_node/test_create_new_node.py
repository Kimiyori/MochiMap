from uuid import uuid4

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from src.infrastructure.persistence.models.node.node import NodeModel
from src.modules.roadmap.domain.node.value_objects import NodeType
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap


class TestCreateNewNodeUseCase:
    @pytest.mark.parametrize("num_roadmaps,model", [(1, NodeModel)])
    async def test_create_learning_note_node_success(
        self, faker: Faker, client: AsyncClient, created_roadmaps: list[Roadmap], check_if_exists
    ) -> None:
        roadmap_id = created_roadmaps[0].id
        data = {
            "type": NodeType.LEARNING_NOTE,
            "data": {"title": faker.sentence(), "content": faker.paragraph()},
            "position_x": faker.random_int(min=0, max=100),
            "position_y": faker.random_int(min=0, max=100),
        }

        response = await client.post(f"/roadmap/{roadmap_id}/node", json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert await check_if_exists()

    @pytest.mark.parametrize("num_roadmaps,model", [(1, NodeModel)])
    async def test_create_resource_bookmark_node_success(
        self, faker: Faker, client: AsyncClient, created_roadmaps: list[Roadmap], check_if_exists
    ) -> None:
        roadmap_id = created_roadmaps[0].id
        data = {
            "type": NodeType.RESOURCE_BOOKMARK,
            "data": {"title": faker.sentence(), "url": faker.url()},
            "position_x": faker.random_int(min=0, max=100),
            "position_y": faker.random_int(min=0, max=100),
        }
        response = await client.post(f"/roadmap/{roadmap_id}/node", json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert await check_if_exists()


class TestCreateNewNodeErrorUseCase:
    async def test_create_node_non_existent_roadmap_fails(self, faker: Faker, client: AsyncClient) -> None:
        non_existent_roadmap_id = 11
        data = {
            "type": NodeType.LEARNING_NOTE,
            "data": {"title": faker.sentence(), "content": faker.paragraph()},
            "position_x": faker.random_int(min=0, max=100),
            "position_y": faker.random_int(min=0, max=100),
        }

        response = await client.post(f"/roadmap/{non_existent_roadmap_id}/node", json=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize("num_roadmaps", [1])
    async def test_create_node_missing_required_fields_fails(
        self, faker: Faker, client: AsyncClient, created_roadmaps: list[Roadmap]
    ) -> None:
        roadmap_id = created_roadmaps[0].id
        data = {
            "type": NodeType.LEARNING_NOTE,
            "data": {
                # "title" is missing
                "content": faker.paragraph()
            },
            "position_x": faker.random_int(min=0, max=100),
            "position_y": faker.random_int(min=0, max=100),
        }
        response = await client.post(f"/roadmap/{roadmap_id}/node", json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_node_invalid_node_type_fails(self, faker: Faker, client: AsyncClient) -> None:
        data = {
            "type": "INVALID_TYPE",
            "data": {"title": faker.sentence()},
            "position_x": faker.random_int(min=0, max=100),
            "position_y": faker.random_int(min=0, max=100),
        }

        response = await client.post(f"/roadmap/{uuid4()}/node", json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_resource_node_missing_url_fails(self, faker: Faker, client: AsyncClient) -> None:
        data = {
            "type": NodeType.RESOURCE_BOOKMARK,
            "data": {
                "title": faker.sentence(),
            },
            "position_x": faker.random_int(min=0, max=100),
            "position_y": faker.random_int(min=0, max=100),
        }

        response = await client.post(f"/roadmap/{uuid4()}/node", json=data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
