from infrastructure.persistence.base.base_repository import SqlAlchemyRepository
from modules.roadmap.domain.roadmap import Roadmap


class BaseRoadmapRepository(SqlAlchemyRepository[Roadmap]):
    model = Roadmap
