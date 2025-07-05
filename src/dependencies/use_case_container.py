from dependency_injector import providers
from dependency_injector.containers import copy

from src.dependencies.base_container import BaseContainer
from src.modules.roadmap.use_cases.create_roadmap.impl import CreateRoadmapUseCase
from src.modules.roadmap.use_cases.get_all_user_roadmaps.impl import GetUserRoadmapsUseCase


@copy(BaseContainer)
class UseCaseContainer(BaseContainer):

    # ROADMAP
    create_roadmap_use_case = providers.Factory(CreateRoadmapUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
    get_user_roadmaps_use_case = providers.Factory(GetUserRoadmapsUseCase, uow=BaseContainer.infrastructure.roadmap_uow)

    