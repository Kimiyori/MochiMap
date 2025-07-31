import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.persistence.models.base_model import Base, UUIDMixin


class ConnectionModel(Base, UUIDMixin):
    __tablename__ = "connections"

    roadmap_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roadmaps.id"), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)

