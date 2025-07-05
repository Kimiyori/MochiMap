from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.persistence.models.roadmap.repository import BaseRoadmapRepository
from src.infrastructure.persistence.transaction.unit_of_work import SqlAlchemyUnitOfWork


class RoadmapUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine)
        self.repository = BaseRoadmapRepository(self.session)

