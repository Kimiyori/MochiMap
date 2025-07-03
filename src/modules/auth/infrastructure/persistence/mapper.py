
from sqlalchemy.orm import registry

from infrastructure.persistence.models.user import UserTable
from modules.auth.domain.user import User

mapper_registry = registry()

def start_mapper():
    u = UserTable.__table__

    mapper_registry.map_imperatively(
        User,
        u,
    )
