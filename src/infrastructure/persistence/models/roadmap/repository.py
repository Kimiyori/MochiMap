from sqlalchemy import exists, func, select

from src.infrastructure.persistence.base.base_repository import SqlAlchemyRepository
from src.modules.roadmap.domain.edge.edge import Edge
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.roadmap.roadmap import Roadmap


class BaseRoadmapRepository(SqlAlchemyRepository[Roadmap]):
    model = Roadmap

    async def nodes_exist_in_roadmap(self, roadmap_id: str, node_ids: list[str]) -> bool:
        if not node_ids:
            return False
        stmt = select(func.count()).where(Node.roadmap_id == roadmap_id, Node.id.in_(node_ids))
        result = await self.session.execute(stmt)
        count = int(result.scalar() or 0)
        return count == len(set(node_ids))

    async def edge_exists(self, roadmap_id: str, source_id: str, target_id: str) -> bool:
        stmt = select(
            exists().where(
                Edge.roadmap_id == roadmap_id,
                Edge.source_id == source_id,
                Edge.target_id == target_id,
            )
        )
        result = await self.session.execute(stmt)
        return bool(result.scalar())
