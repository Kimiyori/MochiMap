import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.persistence.models.base_model import Base, UUIDMixin

if TYPE_CHECKING:
    from src.infrastructure.persistence.models.roadmap.roadmap import RoadmapModel


class EdgeModel(Base, UUIDMixin):
    __tablename__ = "edges"

    roadmap_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roadmaps.id"), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)

    roadmap: Mapped["RoadmapModel"] = relationship(back_populates="edges")
