import pytest
from sqlalchemy import select

from src.infrastructure.persistence.models.base_model import Base
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


@pytest.fixture
def created_roadmaps(session, num_roadmaps: int) -> list[Roadmap]:
    roadmaps: list[Roadmap] = []

    for i in range(num_roadmaps):
        command = CreateRoadmapCommand(
            title=f"Test Roadmap {i + 1}", description=f"Test description for roadmap {i + 1}"
        )

        roadmap = Roadmap.new_roadmap(command)
        session.add(roadmap)
        roadmaps.append(roadmap)

    return roadmaps

@pytest.fixture
def check_if_exists(session, model: Base):
    """Fixture to check if a roadmap exists by ID."""

    async def _check_if_exists() -> bool:
        result = await session.execute(select(model))
        data = result.scalars().all()
        return len(data) == 1

    return _check_if_exists
