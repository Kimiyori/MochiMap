from uuid import UUID

from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.use_cases.get_roadmap_nodes.response_dto import GetRoadmapNodesResponseDTO


class GetRoadmapNodesUseCase(BaseUseCase):
    def __init__(self, uow: SqlAlchemyUnitOfWork[Node]) -> None:
        self.uow = uow

    @async_transactional(read_only=True)
    async def invoke(self, roadmap_id: UUID) -> list[GetRoadmapNodesResponseDTO]:
        return await self.uow.repository.get_all_by_field("roadmap_id", roadmap_id)
