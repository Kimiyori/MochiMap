from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.modules.roadmap.infrastructure.persistence.edge_repository import EdgeRepository
from src.modules.roadmap.infrastructure.persistence.node_repository import NodeRepository
from src.modules.roadmap.infrastructure.persistence.roadmap_repository import RoadmapRepository


class RoadmapUnitOfWork(SqlAlchemyUnitOfWork[RoadmapRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, RoadmapRepository)


class NodeUnitOfWork(SqlAlchemyUnitOfWork[NodeRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, NodeRepository)


class EdgeUnitOfWork(SqlAlchemyUnitOfWork[EdgeRepository]):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine, EdgeRepository)
