from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.common.errors import NotFoundException
from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.models.roadmap.roadmap import RoadmapModel
from src.infrastructure.persistence.transaction import async_transactional
from src.modules.roadmap.infrastructure.uow import RoadmapUnitOfWork
from src.modules.roadmap.use_cases.get_roadmap_data.response_dto import GetRoadmapNodesResponseDTO


class GetRoadmapDataUseCase(BaseUseCase[RoadmapUnitOfWork]):
    
    @async_transactional(read_only=True)
    async def invoke(self, roadmap_id: UUID) -> list[GetRoadmapNodesResponseDTO]:
        query = (
            select(RoadmapModel)
            .where(RoadmapModel.id == roadmap_id)
            .options(
                joinedload(RoadmapModel.nodes),
                joinedload(RoadmapModel.edges),
            )
        )
        data = await self.uow.session.execute(query)
        result = data.scalar()
        if result is None:
            raise NotFoundException(f"Roadmap with id {roadmap_id} not found")
        return result
