import pytest

from src.modules.roadmap.domain.roadmap.roadmap import Roadmap
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


@pytest.fixture
def created_roadmaps_with_some_empty_descriptions(session, num_roadmaps: int) -> list[Roadmap]:
    roadmaps: list[Roadmap] = []

    for i in range(num_roadmaps):
        command = CreateRoadmapCommand(
            title=f"Test Roadmap {i + 1}", description=None if i % 2 == 0 else f"Test description for roadmap {i + 1}"
        )

        roadmap = Roadmap.new_roadmap(command)
        session.add(roadmap)
        roadmaps.append(roadmap)

    return roadmaps
