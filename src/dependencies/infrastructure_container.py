from dependency_injector import containers, providers
from dependency_injector.providers import Singleton

from src.core.config import DB_SETTINGS
from src.infrastructure.persistence.engine import AsyncDatabase
from src.modules.roadmap.infrastructure.uow import EdgeUnitOfWork, NodeUnitOfWork, RoadmapUnitOfWork


class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.DependenciesContainer()

    # Core infrastructure
    db = Singleton(AsyncDatabase, db_uri=DB_SETTINGS.database_uri)

    # Unit of Work

    roadmap_uow = providers.Factory(
        RoadmapUnitOfWork,
        engine=db.provided.engine,
    )
    node_uow = providers.Factory(
        NodeUnitOfWork,
        engine=db.provided.engine,
    )
    edge_uow = providers.Factory(
        EdgeUnitOfWork,
        engine=db.provided.engine,
    )
