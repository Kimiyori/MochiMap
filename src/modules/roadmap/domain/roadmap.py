from dataclasses import dataclass, field
from uuid import UUID
from xml.dom import Node

from modules.roadmap.domain.value_objects import Connection, Difficulty, EstimatedTime, TimeUnit
from modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


@dataclass
class Roadmap:
    id: UUID
    title: str
    description: str
    owner_id: UUID
    difficulty: Difficulty
    estimated_time: EstimatedTime
    estimated_time_unit: TimeUnit
    nodes: list[Node] =  field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)

    @staticmethod
    def new_roadmap(command: CreateRoadmapCommand) -> "Roadmap":
        return Roadmap(
            id=command.id,
            title=command.title,
            description=command.description,
            owner_id=command.owner_id,
            difficulty=command.difficulty,
            estimated_time=command.estimated_time,
            estimated_time_unit=command.estimated_time_unit,
        )
