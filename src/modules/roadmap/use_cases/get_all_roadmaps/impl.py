from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.modules.roadmap.infrastructure.uow import RoadmapUnitOfWork


class GetUserRoadmapsUseCase(BaseUseCase[RoadmapUnitOfWork]):

    @async_transactional(read_only=True)
    async def invoke(self):
        return await self.uow.repository.get_all()
