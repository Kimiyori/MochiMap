from src.common.protocols.use_case import BaseUseCase
from src.infrastructure.persistence.transaction import async_transactional
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


class CreateRoadmapUseCase(BaseUseCase):
    def __init__(self, uow: SqlAlchemyUnitOfWork) -> None:
        self.uow = uow

    @async_transactional()
    async def invoke(self, data: CreateRoadmapCommand) -> None:
        new_roadmap=Roadmap.new_roadmap(data)
        self.uow.repository.add(new_roadmap)

