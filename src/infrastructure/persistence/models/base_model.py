from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID, DateTime, MetaData, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, registry

metadata = MetaData()
mapper_registry = registry(metadata=metadata)
SQLBase = mapper_registry.generate_base()


class TimestampMixin:
    """Mixin that adds created_at and updated_at columns to models."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class UUIDMixin:
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class Base(AsyncAttrs, SQLBase):
    """Base class for all models."""

    __abstract__ = True
