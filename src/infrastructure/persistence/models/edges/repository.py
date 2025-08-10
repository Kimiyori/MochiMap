from src.infrastructure.persistence.base.base_repository import SqlAlchemyRepository
from src.modules.roadmap.domain.edge.edge import Edge


class BaseEdgeRepository(SqlAlchemyRepository[Edge]):
    model = Edge
