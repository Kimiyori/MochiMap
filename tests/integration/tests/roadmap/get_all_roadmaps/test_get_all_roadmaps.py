import pytest
from fastapi import status
from httpx import AsyncClient


class TestGetAllRoadmapsUseCase:
    async def test_get_all_roadmaps_empty_list_success(self, client:AsyncClient) -> None:
        response = await client.get("/roadmap")

        assert response.status_code == status.HTTP_200_OK
        roadmaps = response.json()
        assert isinstance(roadmaps, list)
        assert len(roadmaps) == 0

    @pytest.mark.parametrize("num_roadmaps", [1])
    async def test_get_all_roadmaps_single_roadmap_success(self, client:AsyncClient, created_roadmaps) -> None:
        response = await client.get("/roadmap")

        assert response.status_code == status.HTTP_200_OK
        roadmaps = response.json()
        assert isinstance(roadmaps, list)
        assert len(roadmaps) == 1

        roadmap = roadmaps[0]
        assert roadmap["title"] == created_roadmaps[0].title
        assert roadmap["description"] == created_roadmaps[0].description
        assert roadmap["id"] == str(created_roadmaps[0].id)

    @pytest.mark.parametrize("num_roadmaps", [3])
    async def test_get_all_roadmaps_multiple_roadmaps_success(self, client:AsyncClient, created_roadmaps) -> None:
        response = await client.get("/roadmap")

        assert response.status_code == status.HTTP_200_OK
        roadmaps = response.json()
        assert isinstance(roadmaps, list)
        assert len(roadmaps) == len(created_roadmaps)

        for expected_roadmap, created_roadmap in zip(roadmaps, created_roadmaps, strict=False):
            assert expected_roadmap["title"] == created_roadmap.title
            assert expected_roadmap["description"] == created_roadmap.description
            assert expected_roadmap["id"] == str(created_roadmap.id)

    @pytest.mark.parametrize("num_roadmaps", [3])
    async def test_get_all_roadmaps_with_empty_descriptions(
        self, client:AsyncClient, created_roadmaps_with_some_empty_descriptions
    ) -> None:
        response = await client.get("/roadmap")

        assert response.status_code == status.HTTP_200_OK
        roadmaps = response.json()
        assert len(roadmaps) == len(created_roadmaps_with_some_empty_descriptions)

        for expected_roadmap, created_roadmap in zip(
            roadmaps, created_roadmaps_with_some_empty_descriptions, strict=False
        ):
            assert expected_roadmap["title"] == created_roadmap.title
            assert expected_roadmap["description"] == created_roadmap.description
            assert expected_roadmap["id"] == str(created_roadmap.id)
       