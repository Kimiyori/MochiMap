from typing import TYPE_CHECKING
from uuid import UUID

import pytest

from src.modules.roadmap.domain.roadmap.errors import RoadmapValidationError
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap

if TYPE_CHECKING:
    from faker import Faker

    from tests.unit.roadmap.entities.conftest import RoadmapTestDataFactory

class TestRoadmapCreation:
    def test_new_roadmap_creates_roadmap_with_expected_fields(
        self,
        created_roadmap: Roadmap,
    ):
        roadmap = created_roadmap

        assert isinstance(roadmap, Roadmap)
        assert isinstance(roadmap.title, str)
        assert isinstance(roadmap.description, str)
        assert isinstance(roadmap.id, UUID)
        assert roadmap.nodes == []

    def test_new_roadmap_with_minimal_data(
        self,
        roadmap_factory: "RoadmapTestDataFactory",
        fake: "Faker",
    ):
        title = fake.word()
        roadmap = roadmap_factory.create_roadmap(title=title, description="")

        assert roadmap.title == title
        assert roadmap.description == ""
        assert roadmap.nodes == []

    def test_roadmap_with_empty_title(
        self,
        roadmap_factory: "RoadmapTestDataFactory",
    ):
        with pytest.raises(RoadmapValidationError, match="Title must not be empty."):
            roadmap_factory.create_roadmap(title="", description="")
