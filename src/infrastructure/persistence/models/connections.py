import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistence.base.base_entities import Base, UUIDMixin
from modules.roadmap.domain.value_objects import ConnectionType

if TYPE_CHECKING:
    from modules.roadmap.domain.node import NodeModel
    from modules.roadmap.domain.roadmap import RoadmapModel


class ConnectionModel(Base, UUIDMixin):
    __tablename__ = "connections"

    roadmap_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roadmaps.id"), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)
    connection_type: Mapped[ConnectionType] = mapped_column(default=ConnectionType.SEQUENTIAL)
    label: Mapped[str] = mapped_column(String, default="")

    # Relationships
    roadmap: Mapped["RoadmapModel"] = relationship(back_populates="connections")
    source_node: Mapped["NodeModel"] = relationship(foreign_keys=[source_id])
    target_node: Mapped["NodeModel"] = relationship(foreign_keys=[target_id])
