
from uuid import UUID

from src.common.errors import NotFoundException
from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.modules.roadmap.infrastructure.uow import NodeUnitOfWork


class DeleteNodeUseCase(BaseUseCase[NodeUnitOfWork]):
    @async_transactional()
    async def invoke(self, node_id: UUID):
        node = await self.uow.repository.get_by_field("id", str(node_id))
        if not node:
            raise NotFoundException(f"Node with id {node_id} not found")

        await self.uow.repository.delete(node)