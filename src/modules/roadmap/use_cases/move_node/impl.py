from uuid import UUID

from src.common.errors import NotFoundException
from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.use_cases.move_node.command import MoveNodeCommand


class MoveNodeUseCase(BaseUseCase):
    def __init__(self, uow: SqlAlchemyUnitOfWork[Node]) -> None:
        self.uow = uow

    @async_transactional()
    async def invoke(self, node_id: UUID, data: MoveNodeCommand) -> None:
        node = await self.uow.repository.get_by_field("id", node_id)
        if not node:
            raise NotFoundException(f"Node with id {node_id} not found")

        node.move_node(data)
        self.uow.repository.add(node)
