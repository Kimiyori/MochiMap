from dependency_injector import containers, providers
from dependency_injector.providers import Singleton

from core.config import DB_SETTINGS
from infrastructure.adapters.keycloak import KeycloakClient
from infrastructure.persistence.connection.connection import AsyncDatabase
from infrastructure.persistence.transaction.unit_of_work import SqlAlchemyUnitOfWork
from modules.roadmap.infrastructure.uow import RoadmapUnitOfWork


class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.DependenciesContainer()

    # Core infrastructure
    db = Singleton(AsyncDatabase, db_uri=DB_SETTINGS.database_uri)

    auth = Singleton(KeycloakClient, auth_config=config.auth_config)
    # Unit of Work
    uow = providers.Factory(
        SqlAlchemyUnitOfWork,
        engine=db.provided.engine,
    )
    roadmap_uow = providers.Factory(
        RoadmapUnitOfWork,
        engine=db.provided.engine,
    )
