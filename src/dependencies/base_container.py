from dependency_injector import containers, providers

from dependencies.config_container import ConfigContainer
from dependencies.infrastructure_container import InfrastructureContainer


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Container(ConfigContainer)

    infrastructure = providers.Container(InfrastructureContainer, config=config)
