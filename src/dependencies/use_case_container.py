from dependency_injector import providers
from dependency_injector.containers import copy

from src.dependencies.base_container import BaseContainer
from src.modules.roadmap.use_cases.create_new_node.impl import CreateNodeUseCase
from src.modules.roadmap.use_cases.create_roadmap.impl import CreateRoadmapUseCase
from src.modules.roadmap.use_cases.get_all_roadmaps.impl import GetUserRoadmapsUseCase
from src.modules.roadmap.use_cases.get_roadmap_nodes.impl import GetRoadmapNodesUseCase


@copy(BaseContainer)
class UseCaseContainer(BaseContainer):

    # ROADMAP
    create_roadmap_use_case = providers.Factory(CreateRoadmapUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
    create_node_use_case = providers.Factory(CreateNodeUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
    get_user_roadmaps_use_case = providers.Factory(GetUserRoadmapsUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
    get_roadmap_nodes_use_case = providers.Factory(
        GetRoadmapNodesUseCase, uow=BaseContainer.infrastructure.node_uow
    )
