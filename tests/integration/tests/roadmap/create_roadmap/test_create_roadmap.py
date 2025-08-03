import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from src.infrastructure.persistence.models.roadmap.roadmap import RoadmapModel
from src.modules.roadmap.domain.roadmap.errors import RoadmapValidationError


class TestCreateRoadmapUseCase:
    @pytest.mark.parametrize("model", [RoadmapModel])
    async def test_create_roadmap_with_valid_data_success(self,faker:Faker, client:AsyncClient, check_if_exists) -> None:
        data = {
            "title": faker.sentence(),
            "description": faker.paragraph(),
        }
        response = await client.post("/roadmap/", json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert await check_if_exists() is True

    @pytest.mark.parametrize("model", [RoadmapModel])
    async def test_create_roadmap_with_empty_description(self,faker:Faker, client:AsyncClient, check_if_exists) -> None:
        data = {"title": faker.sentence(), "description": None}
        response = await client.post("/roadmap/", json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert await check_if_exists() is True

    @pytest.mark.parametrize("model", [RoadmapModel])
    async def test_create_roadmap_without_description(self,faker:Faker, client:AsyncClient, check_if_exists) -> None:
        data = {"title": faker.sentence()}
        response = await client.post("/roadmap/", json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert await check_if_exists() is True


class TestCreateRoadmapErrorUseCase:
    async def test_create_roadmap_missing_title_fails(self, client) -> None:
        response = await client.post("/roadmap/", json={"description": "Missing title field"})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_roadmap_empty_title_fails(self, faker:Faker, client:AsyncClient) -> None:
        with pytest.raises(RoadmapValidationError):
            await client.post("/roadmap/", json={"title": "", "description": faker.paragraph()})

    async def test_create_roadmap_whitespace_title_fails(self,faker:Faker, client:AsyncClient) -> None:
        with pytest.raises(RoadmapValidationError):
            await client.post("/roadmap/", json={"title": "   ", "description": faker.paragraph()})
