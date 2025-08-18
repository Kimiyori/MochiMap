from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.common.errors import NotFoundException
from src.common.openapi import error_responses
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand
from src.modules.roadmap.use_cases.create_new_node.impl import CreateNodeUseCase
from src.modules.roadmap.use_cases.create_new_node.response_dto import CreateNewNodeResponseDTO


@roadmap_router.post(
    path="/{roadmap_id:uuid}/node",
    name="Create New Node",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateNewNodeResponseDTO,
    responses=error_responses(NotFoundException),
)
@inject
async def create_new_node(
    roadmap_id: UUID,
    data: CreateNodeCommand,
    uc: Annotated[CreateNodeUseCase, Depends(Provide["roadmap.create_node_use_case"])],
):
    return await uc.invoke(roadmap_id, data)
