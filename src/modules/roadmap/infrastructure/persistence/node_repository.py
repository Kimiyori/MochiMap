from src.infrastructure.persistence.base.base_repository import SqlAlchemyRepository
from src.modules.roadmap.domain.node.node import Node


class BaseNodeRepository(SqlAlchemyRepository[Node]):
    model = Node
