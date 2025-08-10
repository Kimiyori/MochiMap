from dependency_injector import providers
from dependency_injector.containers import copy

from src.dependencies.base_container import BaseContainer
from src.modules.roadmap.use_cases.create_edge.impl import CreateEdgeUseCase
from src.modules.roadmap.use_cases.create_new_node.impl import CreateNodeUseCase
from src.modules.roadmap.use_cases.create_roadmap.impl import CreateRoadmapUseCase
from src.modules.roadmap.use_cases.get_all_roadmaps.impl import GetUserRoadmapsUseCase
from src.modules.roadmap.use_cases.get_roadmap_data.impl import GetRoadmapDataUseCase
from src.modules.roadmap.use_cases.move_node.impl import MoveNodeUseCase


@copy(BaseContainer)
class UseCaseContainer(BaseContainer):
    # ROADMAP
    create_roadmap_use_case = providers.Factory(CreateRoadmapUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
    create_node_use_case = providers.Factory(CreateNodeUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
    create_edge_use_case = providers.Factory(CreateEdgeUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
    move_node_use_case = providers.Factory(MoveNodeUseCase, uow=BaseContainer.infrastructure.node_uow)

    get_user_roadmaps_use_case = providers.Factory(GetUserRoadmapsUseCase, uow=BaseContainer.infrastructure.roadmap_uow)
    get_roadmap_nodes_use_case = providers.Factory(GetRoadmapDataUseCase, uow=BaseContainer.infrastructure.node_uow)
