
from uuid import UUID

from src.common.errors import NotFoundException
from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.modules.roadmap.infrastructure.uow import EdgeUnitOfWork


class DeleteEdgeUseCase(BaseUseCase[EdgeUnitOfWork]):
    @async_transactional()
    async def invoke(self, edge_id: UUID):
        edge = await self.uow.repository.get_by_field("id", str(edge_id))
        if not edge:
            raise NotFoundException(f"Edge with id {edge_id} not found")

        await self.uow.repository.delete(edge)