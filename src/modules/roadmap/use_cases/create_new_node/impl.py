from uuid import UUID

from src.common.errors import NotFoundException
from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.modules.roadmap.infrastructure.uow import RoadmapUnitOfWork
from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand


class CreateNodeUseCase(BaseUseCase[RoadmapUnitOfWork]):

    @async_transactional()
    async def invoke(self, roadmap_id: UUID, data: CreateNodeCommand) -> dict[str, UUID]:
        roadmap = await self.uow.repository.get_by_field("id", roadmap_id)
        if not roadmap:
            raise NotFoundException(f"Roadmap with id {roadmap_id} not found")
        new_node = roadmap.create_node(data)
        self.uow.repository.add(new_node)
        return {"id": new_node.id}
