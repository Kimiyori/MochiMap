from sqlalchemy.orm import composite

from src.infrastructure.persistence.base.base_entities import mapper_registry
from src.infrastructure.persistence.models.roadmap.roadmap import RoadmapModel
from src.modules.roadmap.domain.roadmap import Roadmap
from src.modules.roadmap.domain.value_objects import Difficulty, EstimatedTime


def start_mapper():

    # Roadmap mapper
    mapper_registry.map_imperatively(
        Roadmap,
        RoadmapModel.__table__,
           properties={
            # Map value objects to database columns
            'difficulty': composite(
                Difficulty,
                RoadmapModel.__table__.c.difficulty_level,
            ),
            'estimated_time': composite(
                EstimatedTime,
                RoadmapModel.__table__.c.estimated_time_value,
                RoadmapModel.__table__.c.estimated_time_unit,
            ),
        }
    )