
import uuid

from fastapi import status

from src.modules.roadmap.domain.value_objects import Difficulty, EstimatedTime, TimeUnit
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


class TestCreateRoadmapUseCase:
    path_prefix = "/vacancy"

    async def _create_roadmap(self, async_client, uuid):
        """Helper method to delete a specific vacancy"""
        response = await async_client.delete(f"{self.path_prefix}/{uuid}")
        return response

    async def test_create_roadmap_ok(self, async_client):
        """Test that the endpoint returns a 200 OK status code when deleting a valid vacancy"""
        data = CreateRoadmapCommand(
            title="Test Roadmap",
            description="This is a test roadmap",
            owner_id=uuid.uuid4(),
            difficulty=Difficulty.EASY,
            estimated_time=EstimatedTime(2,TimeUnit.HOURS),
        )
        response = await self._create_roadmap(async_client, 1)
        assert response.status_code == status.HTTP_201_CREATED
