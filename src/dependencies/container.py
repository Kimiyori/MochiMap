from pathlib import Path

from dependency_injector.containers import WiringConfiguration, copy

from core.routes import discover_api_modules
from dependencies.use_case_container import UseCaseContainer


@copy(UseCaseContainer)
class Container(UseCaseContainer):
    
    wiring_config = WiringConfiguration(
        modules=discover_api_modules(Path(__file__).parent.parent),
    )
