from uuid import UUID

from src.common.errors import BadRequestException, ConflictException, NotFoundException
from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.modules.roadmap.domain.edge.errors import SelfLoopEdgeError
from src.modules.roadmap.infrastructure.uow import RoadmapUnitOfWork
from src.modules.roadmap.use_cases.create_edge.command import CreateEdgeCommand


class CreateEdgeUseCase(BaseUseCase[RoadmapUnitOfWork]):

    @async_transactional()
    async def invoke(self, roadmap_id: UUID, data: CreateEdgeCommand) -> dict[str, UUID]:
        roadmap = await self.uow.repository.get_by_field("id", str(roadmap_id))
        if not roadmap:
            raise NotFoundException(f"Roadmap with id {roadmap_id} not found")

        both_exist = await self.uow.repository.nodes_exist_in_roadmap(
            str(roadmap_id), [str(data.source_id), str(data.target_id)]
        )
        if not both_exist:
            raise NotFoundException("Source and target must belong to the specified roadmap")

        if await self.uow.repository.edge_exists(str(roadmap_id), str(data.source_id), str(data.target_id)):
            raise ConflictException("Edge with the same source and target already exists")

        try:
            edge = roadmap.create_edge(data.source_id, data.target_id)
        except SelfLoopEdgeError as e:
            raise BadRequestException(str(e)) from None
        self.uow.repository.add(edge)
        return {"id": edge.id}
