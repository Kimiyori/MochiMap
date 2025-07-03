import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistence.base.base_entities import Base, IdMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import User


class AuthProviderEnum(enum.Enum):
    LOCAL = "local"
    GOOGLE = "google"
    TWITTER = "twitter"
    GITHUB = "github"


class UserAuthProviderTable(Base, IdMixin, TimestampMixin):
    __tablename__ = "user_auth_providers"

    __table_args__ = (UniqueConstraint("provider", "provider_user_id", name="_provider_user_unique"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    provider: Mapped[AuthProviderEnum] = mapped_column(Enum(AuthProviderEnum), nullable=False, index=True)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="auth_providers")

    def __repr__(self) -> str:
        return f"<UserAuthProvider {self.provider}:{self.provider_user_id} for user {self.user_id}>"
