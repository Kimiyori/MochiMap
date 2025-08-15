from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.modules.roadmap.infrastructure.persistence.edge_repository import BaseEdgeRepository
from src.modules.roadmap.infrastructure.persistence.node_repository import BaseNodeRepository
from src.modules.roadmap.infrastructure.persistence.roadmap_repository import BaseRoadmapRepository


class RoadmapUnitOfWork(SqlAlchemyUnitOfWork[BaseRoadmapRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, BaseRoadmapRepository)


class NodeUnitOfWork(SqlAlchemyUnitOfWork[BaseNodeRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, BaseNodeRepository)


class EdgeUnitOfWork(SqlAlchemyUnitOfWork[BaseEdgeRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, BaseEdgeRepository)
