import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.persistence.models.base_model import Base, UUIDMixin
from src.modules.roadmap.domain.edge.value_objects import EdgeType

if TYPE_CHECKING:
    from src.infrastructure.persistence.models.node.node import NodeModel
    from src.infrastructure.persistence.models.roadmap.roadmap import RoadmapModel

SQL_EDGE_TYPE = Enum(EdgeType, name="edge_type")

class EdgeModel(Base, UUIDMixin):
    __tablename__ = "edges"

    roadmap_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roadmaps.id"), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)
    type: Mapped[EdgeType] = mapped_column( nullable=False, server_default=EdgeType.BEZIER.value)
    target_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)

    roadmap: Mapped["RoadmapModel"] = relationship(back_populates="edges")
    source: Mapped["NodeModel"] = relationship(
        "NodeModel",
        foreign_keys=[source_id],
        back_populates="outgoing_edges",
    )
    target: Mapped["NodeModel"] = relationship(
        "NodeModel",
        foreign_keys=[target_id],
        back_populates="incoming_edges",
    )