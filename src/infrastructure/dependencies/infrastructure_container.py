from dependency_injector import containers, providers
from dependency_injector.providers import Singleton

from src.core.config import DB_SETTINGS
from src.infrastructure.persistence.engine import AsyncDatabase


class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.DependenciesContainer()

    # Core infrastructure
    db = Singleton(AsyncDatabase, db_uri=DB_SETTINGS.database_uri)

    # Note: UoWs are module-specific; they live in each module container
