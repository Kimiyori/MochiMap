from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.dependencies.container import Container
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.create_new_node.command import CreateNodeCommand
from src.modules.roadmap.use_cases.create_new_node.impl import CreateNodeUseCase


@roadmap_router.post(path="/{roadmap_id:uuid}/node", name="Create New Node", status_code=status.HTTP_201_CREATED)
@inject
async def create_new_node(
    roadmap_id: UUID,
    data: CreateNodeCommand,
    uc: Annotated[CreateNodeUseCase, Depends(Provide[Container.create_node_use_case])],
):
    return await uc.invoke(roadmap_id,data)
