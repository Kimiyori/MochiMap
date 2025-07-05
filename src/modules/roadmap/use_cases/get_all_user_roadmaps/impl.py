from uuid import UUID

from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction.transaction import async_transactional
from src.infrastructure.persistence.transaction.unit_of_work import SqlAlchemyUnitOfWork


class GetUserRoadmapsUseCase(BaseUseCase):
    def __init__(self, uow: SqlAlchemyUnitOfWork) -> None:
        self.uow = uow

    @async_transactional(read_only=True)
    async def invoke(self, owner_id: UUID) -> None:
        return await self.uow.repository.get_all_by_field('owner_id', owner_id)

