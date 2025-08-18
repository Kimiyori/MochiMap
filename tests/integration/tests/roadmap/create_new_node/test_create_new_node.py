from uuid import UUID, uuid4

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from src.infrastructure.persistence.models.node.node import NodeModel
from src.modules.roadmap.domain.node.value_objects import NodeType
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap


async def make_request( client: AsyncClient, roadmap_id: UUID, data: dict):
    return await client.post(f"/roadmap/{roadmap_id}/node", json=data)


@pytest.mark.parametrize("model", [NodeModel])
class TestCreateNewNodeUseCase:

    @pytest.mark.usefixtures("check_if_exists")
    async def test_create_learning_note_node_success(
        self, faker: Faker, client: AsyncClient, created_roadmaps: list[Roadmap]
    ) -> None:
        roadmap_id = created_roadmaps[0].id
        data = {
            "type": NodeType.LEARNING_NOTE,
            "data": {"title": faker.sentence(), "content": faker.paragraph()},
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=100),
                "y": faker.pyfloat(min_value=0, max_value=100),
            },
        }

        response = await make_request(client, roadmap_id, data)

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.usefixtures("check_if_exists")
    async def test_create_resource_bookmark_node_success(
        self, faker: Faker, client: AsyncClient, created_roadmaps: list[Roadmap]
    ) -> None:
        roadmap_id = created_roadmaps[0].id
        data = {
            "type": NodeType.RESOURCE_BOOKMARK,
            "data": {"title": faker.sentence(), "url": faker.url()},
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=100),
                "y": faker.pyfloat(min_value=0, max_value=100),
            },
        }
        response = await make_request(client, roadmap_id, data)

        assert response.status_code == status.HTTP_201_CREATED


class TestCreateNewNodeErrorUseCase:
    async def test_create_node_non_existent_roadmap_fails(self, faker: Faker, client: AsyncClient) -> None:
        non_existent_roadmap_id = 11
        data = {
            "type": NodeType.LEARNING_NOTE,
            "data": {"title": faker.sentence(), "content": faker.paragraph()},
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=100),
                "y": faker.pyfloat(min_value=0, max_value=100),
            },
        }

        response = await make_request(client, non_existent_roadmap_id, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize("num_roadmaps", [1])
    async def test_create_node_missing_required_fields_fails(
        self, faker: Faker, client: AsyncClient, created_roadmaps: list[Roadmap]
    ) -> None:
        roadmap_id = created_roadmaps[0].id
        data = {
            "type": NodeType.LEARNING_NOTE,
            "data": {"content": faker.paragraph()},
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=100),
                "y": faker.pyfloat(min_value=0, max_value=100),
            },
        }
        response = await make_request(client, roadmap_id, data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_node_invalid_node_type_fails(self, faker: Faker, client: AsyncClient) -> None:
        data = {
            "type": "INVALID_TYPE",
            "data": {"title": faker.sentence()},
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=100),
                "y": faker.pyfloat(min_value=0, max_value=100),
            },
        }

        response = await make_request(client, uuid4(), data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_resource_node_missing_url_fails(self, faker: Faker, client: AsyncClient) -> None:
        data = {
            "type": NodeType.RESOURCE_BOOKMARK,
            "data": {
                "title": faker.sentence(),
            },
            "position": {
                "x": faker.pyfloat(min_value=0, max_value=100),
                "y": faker.pyfloat(min_value=0, max_value=100),
            },
        }

        response = await make_request(client, uuid4(), data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
