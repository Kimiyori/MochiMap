from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistence.base.base_entities import Base, IdMixin

if TYPE_CHECKING:
    from .user_auth_provider import UserAuthProvider


class UserTable(Base, IdMixin):
    __tablename__ = "user"

    username: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    picture: Mapped[str | None] = mapped_column(String(500), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    verified_email: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    auth_providers: Mapped[list["UserAuthProvider"]] = relationship(
        "UserAuthProvider", back_populates="user", cascade="all, delete-orphan"
    )
