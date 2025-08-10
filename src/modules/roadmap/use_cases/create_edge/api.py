from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.dependencies.container import Container
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.create_edge.command import CreateEdgeCommand, CreateEdgeResponseDTO
from src.modules.roadmap.use_cases.create_edge.impl import CreateEdgeUseCase


@roadmap_router.post(
    path="/{roadmap_id:uuid}/edge",
    name="Create Edge",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateEdgeResponseDTO,
)
@inject
async def create_edge(
    roadmap_id: UUID,
    data: CreateEdgeCommand,
    uc: Annotated[CreateEdgeUseCase, Depends(Provide[Container.create_edge_use_case])],
):
    return await uc.invoke(roadmap_id, data)
