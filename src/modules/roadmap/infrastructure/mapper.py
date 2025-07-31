from sqlalchemy.orm import column_property, composite, relationship

from src.infrastructure.persistence.models.base_model import mapper_registry
from src.infrastructure.persistence.models.node.node import NodeModel
from src.infrastructure.persistence.models.roadmap.roadmap import RoadmapModel
from src.modules.roadmap.domain.node.node import Node
from src.modules.roadmap.domain.node.value_objects import Position
from src.modules.roadmap.domain.roadmap import Roadmap


def start_mapper():
    # Roadmap mapper

    mapper_registry.map_imperatively(
        Roadmap,
        RoadmapModel.__table__,
        properties={"nodes": relationship(Node, primaryjoin="Roadmap.id==Node.roadmap_id", lazy="noload")},
    )

    # Node mapper with composite data field
    mapper_registry.map_imperatively(
        Node,
        NodeModel.__table__,
        properties={
            "position": composite(Position, NodeModel.__table__.c.position_x, NodeModel.__table__.c.position_y),
            "data": column_property(NodeModel.__table__.c.data),
        },
    )
