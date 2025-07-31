from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.modules.roadmap.domain.roadmap import Roadmap


class GetUserRoadmapsUseCase(BaseUseCase):
    def __init__(self, uow: SqlAlchemyUnitOfWork[Roadmap]) -> None:
        self.uow = uow

    @async_transactional(read_only=True)
    async def invoke(self):
        return await self.uow.repository.get_all()
