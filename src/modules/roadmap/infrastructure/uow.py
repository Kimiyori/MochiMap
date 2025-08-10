from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.persistence.models.edges.repository import BaseEdgeRepository
from src.infrastructure.persistence.models.node.repository import BaseNodeRepository
from src.infrastructure.persistence.models.roadmap.repository import BaseRoadmapRepository
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork


class RoadmapUnitOfWork(SqlAlchemyUnitOfWork[BaseRoadmapRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, BaseRoadmapRepository)


class NodeUnitOfWork(SqlAlchemyUnitOfWork[BaseNodeRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, BaseNodeRepository)


class EdgeUnitOfWork(SqlAlchemyUnitOfWork[BaseEdgeRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, BaseEdgeRepository)
