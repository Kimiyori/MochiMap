from sqlalchemy.orm import composite

from infrastructure.persistence.base.base_entities import mapper_registry
from infrastructure.persistence.models.roadmap.roadmap import RoadmapModel
from modules.roadmap.domain.roadmap import Roadmap
from modules.roadmap.domain.value_objects import Difficulty, EstimatedTime


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
            ),
            # Handle the estimated_time_unit field - map it to the same column as estimated_time.unit
            'estimated_time_unit': RoadmapModel.__table__.c.estimated_time_unit,
        }
    )