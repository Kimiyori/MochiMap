from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.dependencies.container import Container
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.get_roadmap_nodes.impl import GetRoadmapNodesUseCase
from src.modules.roadmap.use_cases.get_roadmap_nodes.response_dto import GetRoadmapNodesResponseDTO


@roadmap_router.get(
    path="/{roadmap_id:uuid}/nodes",
    name="Get Roadmap Nodes",
    status_code=status.HTTP_200_OK,
    response_model=list[GetRoadmapNodesResponseDTO],
)
@inject
async def get_roadmap_nodes(
    roadmap_id: UUID,
    uc: Annotated[GetRoadmapNodesUseCase, Depends(Provide[Container.get_roadmap_nodes_use_case])],
):
    return await uc.invoke(roadmap_id)
