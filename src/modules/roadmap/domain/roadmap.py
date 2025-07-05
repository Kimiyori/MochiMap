from dataclasses import dataclass
from uuid import UUID, uuid4

from src.modules.roadmap.domain.value_objects import Difficulty, EstimatedTime
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


@dataclass
class Roadmap:
    id: UUID
    title: str
    description: str
    owner_id: UUID
    difficulty: Difficulty
    estimated_time: EstimatedTime
    # nodes: list[Node] =  field(default_factory=list)
    # connections: list[Connection] = field(default_factory=list)

    @staticmethod
    def new_roadmap(command: CreateRoadmapCommand) -> "Roadmap":
        id = uuid4()
        return Roadmap(
            id=id,
            title=command.title,
            description=command.description,
            owner_id=command.owner_id,
            difficulty=command.difficulty,
            estimated_time=command.estimated_time,
        )
