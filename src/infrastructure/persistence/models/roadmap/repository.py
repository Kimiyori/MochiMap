from src.infrastructure.persistence.base.base_repository import SqlAlchemyRepository
from src.modules.roadmap.domain.roadmap import Roadmap


class BaseRoadmapRepository(SqlAlchemyRepository[Roadmap]):
    model = Roadmap
