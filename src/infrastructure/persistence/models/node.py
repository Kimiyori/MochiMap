
from typing import TYPE_CHECKING

from sqlalchemy import Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistence.base.base_entities import Base, UUIDMixin
from modules.roadmap.domain.value_objects import (
    DifficultyLevel,
    NodeType,
    TimeUnit,
)

if TYPE_CHECKING:
    from infrastructure.persistence.models.resource import ResourceModel
    from infrastructure.persistence.models.roadmap.roadmap import RoadmapModel



class NodeModel(Base,UUIDMixin):
    __tablename__ = "nodes"
    roadmap_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roadmaps.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    node_type: Mapped[NodeType] = mapped_column(Enum(NodeType), nullable=False)
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(Enum(DifficultyLevel), nullable=False)
    estimated_time: Mapped[int | None] = mapped_column(Integer)
    estimated_time_unit: Mapped[TimeUnit | None] = mapped_column(Enum(TimeUnit))
    position_x: Mapped[float] = mapped_column(Float, nullable=False)
    position_y: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    roadmap: Mapped["RoadmapModel"] = relationship(back_populates="nodes")
    resources: Mapped[list["ResourceModel"]] = relationship(back_populates="node", cascade="all, delete-orphan")
