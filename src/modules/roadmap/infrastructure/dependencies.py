from dependency_injector import containers, providers

from src.infrastructure.dependencies.infrastructure_container import InfrastructureContainer
from src.modules.roadmap.infrastructure.uow import EdgeUnitOfWork, NodeUnitOfWork, RoadmapUnitOfWork
from src.modules.roadmap.use_cases.create_edge.impl import CreateEdgeUseCase
from src.modules.roadmap.use_cases.create_new_node.impl import CreateNodeUseCase
from src.modules.roadmap.use_cases.create_roadmap.impl import CreateRoadmapUseCase
from src.modules.roadmap.use_cases.delete_edge.impl import DeleteEdgeUseCase
from src.modules.roadmap.use_cases.delete_node.impl import DeleteNodeUseCase
from src.modules.roadmap.use_cases.get_all_roadmaps.impl import GetUserRoadmapsUseCase
from src.modules.roadmap.use_cases.get_roadmap_data.impl import GetRoadmapDataUseCase
from src.modules.roadmap.use_cases.move_node.impl import MoveNodeUseCase


class RoadmapContainer(containers.DeclarativeContainer):
    infrastructure: InfrastructureContainer = providers.DependenciesContainer()

    # Module UoWs (use shared db engine)
    roadmap_uow = providers.Factory(RoadmapUnitOfWork, engine=infrastructure.db.provided.engine)
    node_uow = providers.Factory(NodeUnitOfWork, engine=infrastructure.db.provided.engine)
    edge_uow = providers.Factory(EdgeUnitOfWork, engine=infrastructure.db.provided.engine)

    # Use cases wired to module UoWs
    create_roadmap_use_case = providers.Factory(CreateRoadmapUseCase, uow=roadmap_uow)
    create_node_use_case = providers.Factory(CreateNodeUseCase, uow=roadmap_uow)
    create_edge_use_case = providers.Factory(CreateEdgeUseCase, uow=roadmap_uow)
    delete_edge_use_case = providers.Factory(DeleteEdgeUseCase, uow=edge_uow)
    delete_node_use_case = providers.Factory(DeleteNodeUseCase, uow=node_uow)
    move_node_use_case = providers.Factory(MoveNodeUseCase, uow=node_uow)

    get_user_roadmaps_use_case = providers.Factory(GetUserRoadmapsUseCase, uow=roadmap_uow)
    get_roadmap_data_use_case = providers.Factory(GetRoadmapDataUseCase, uow=roadmap_uow)
