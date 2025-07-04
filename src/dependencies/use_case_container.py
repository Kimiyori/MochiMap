from dependency_injector import providers
from dependency_injector.containers import copy

from dependencies.base_container import BaseContainer
from modules.roadmap.use_cases.create_roadmap.impl import CreateRoadmapUseCase


@copy(BaseContainer)
class UseCaseContainer(BaseContainer):

    # ROADMAP
    create_roadmap_use_case = providers.Factory(CreateRoadmapUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
