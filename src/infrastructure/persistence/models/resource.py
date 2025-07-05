import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.persistence.base.base_entities import Base, UUIDMixin
from src.modules.roadmap.domain.value_objects import ResourceType

if TYPE_CHECKING:
    from src.infrastructure.persistence.models.node import NodeModel


class ResourceModel(Base, UUIDMixin):
    __tablename__ = "resources"

    node_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("nodes.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    resource_type: Mapped[ResourceType] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    is_free: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    node: Mapped["NodeModel"] = relationship(back_populates="resources")
