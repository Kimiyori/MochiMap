from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.persistence.models.base_model import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.infrastructure.persistence.models.node.node import NodeModel

# SQLAlchemy models
class RoadmapModel(Base,TimestampMixin, UUIDMixin):
    __tablename__ = "roadmaps"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)

    # Relationships
    nodes: Mapped[list["NodeModel"]] = relationship(
        back_populates="roadmap", cascade="all, delete-orphan", overlaps="roadmap,nodes"
    )
    # connections: Mapped[list["ConnectionModel"]] = relationship(back_populates="roadmap", cascade="all, delete-orphan")
