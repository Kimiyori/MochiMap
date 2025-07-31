from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.persistence.models.node.repository import BaseNodeRepository
from src.infrastructure.persistence.models.roadmap.repository import BaseRoadmapRepository
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.roadmap import Roadmap


class RoadmapUnitOfWork(SqlAlchemyUnitOfWork[Roadmap]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, BaseRoadmapRepository)


class NodeUnitOfWork(SqlAlchemyUnitOfWork[Node]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, BaseNodeRepository)
