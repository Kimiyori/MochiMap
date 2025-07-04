from common.protocols.use_case import BaseUseCase
from infrastructure.persistence.transaction.transaction import async_transactional
from infrastructure.persistence.transaction.unit_of_work import SqlAlchemyUnitOfWork
from modules.roadmap.domain.roadmap import Roadmap
from modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand


class CreateRoadmapUseCase(BaseUseCase):
    def __init__(self, uow: SqlAlchemyUnitOfWork) -> None:
        self.uow = uow

    @async_transactional()
    async def invoke(self, data: CreateRoadmapCommand) -> None:
        new_roadmap=Roadmap.new_roadmap(data)
        self.uow.repository.add(new_roadmap)
