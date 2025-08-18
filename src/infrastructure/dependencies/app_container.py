from pathlib import Path

from dependency_injector import containers, providers
from dependency_injector.containers import WiringConfiguration

from src.core.routes import discover_api_modules
from src.infrastructure.dependencies.config_container import ConfigContainer
from src.infrastructure.dependencies.infrastructure_container import InfrastructureContainer
from src.modules.roadmap.infrastructure.dependencies import RoadmapContainer


class AppContainer(containers.DeclarativeContainer):
    # Base/shared containers
    config = providers.Container(ConfigContainer)
    infrastructure = providers.Container(InfrastructureContainer, config=config)

    # Module-specific containers
    roadmap = providers.Container(RoadmapContainer, infrastructure=infrastructure)

    # Wiring for APIs (search from 'src')
    wiring_config = WiringConfiguration(modules=discover_api_modules(Path(__file__).parents[2]))
