from sqlalchemy.ext.asyncio import AsyncEngine

from infrastructure.persistence.models.roadmap.repository import BaseRoadmapRepository
from infrastructure.persistence.transaction.unit_of_work import SqlAlchemyUnitOfWork


class RoadmapUnitOfWork(SqlAlchemyUnitOfWork):
    def __init__(self, engine: AsyncEngine) -> None:
        super().__init__(engine)

    async def __aenter__(self):
        await super().__aenter__()

        self.repository = BaseRoadmapRepository(self.session)