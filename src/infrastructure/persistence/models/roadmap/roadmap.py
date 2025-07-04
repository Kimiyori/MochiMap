import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistence.base.base_entities import Base, UUIDMixin
from modules.roadmap.domain.value_objects import DifficultyLevel, TimeUnit

if TYPE_CHECKING:
    from infrastructure.persistence.models.connections import ConnectionModel
    from modules.roadmap.domain.node import NodeModel

# SQLAlchemy models
class RoadmapModel(Base, UUIDMixin):
    __tablename__ = "roadmaps"
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(nullable=False)
    estimated_time_value: Mapped[int] = mapped_column(Integer)
    estimated_time_unit: Mapped[TimeUnit] = mapped_column()

    
    # Relationships
    nodes: Mapped[list["NodeModel"]] = relationship(back_populates="roadmap", cascade="all, delete-orphan")
    connections: Mapped[list["ConnectionModel"]] = relationship(back_populates="roadmap", cascade="all, delete-orphan")
