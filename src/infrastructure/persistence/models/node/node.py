from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, composite, mapped_column, relationship

from src.infrastructure.persistence.models.base_model import Base, UUIDMixin
from src.modules.roadmap.domain.node.value_objects import NodeType

if TYPE_CHECKING:
    from src.infrastructure.persistence.models.roadmap.roadmap import RoadmapModel


@dataclass
class Point:
    x: float
    y: float



class NodeDataType(TypeDecorator):
    impl = JSONB

    def process_bind_param(self, value, dialect):  # noqa: ARG002
        if value is None:
            return None
        return value.__dict__ if hasattr(value, "__dict__") else value



class NodeModel(Base, UUIDMixin):
    __tablename__ = "nodes"
    roadmap_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roadmaps.id"), nullable=False)
    type: Mapped[NodeType] = mapped_column(String, nullable=False)
    position: Mapped[Point] = composite(
        Point,
        mapped_column("position_x", Float, nullable=False),
        mapped_column("position_y", Float, nullable=False),
    )
    data: Mapped[dict] = mapped_column(NodeDataType, default=dict)

    # Relationships
    roadmap: Mapped["RoadmapModel"] = relationship(back_populates="nodes", overlaps="roadmap,nodes")
