from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.infrastructure.dependencies.app_container import AppContainer  # noqa: F401
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.move_node.command import MoveNodeCommand
from src.modules.roadmap.use_cases.move_node.impl import MoveNodeUseCase


@roadmap_router.put(
    path="/node/{node_id:uuid}/move",
    name="Move node position",
    status_code=status.HTTP_200_OK,
)
@inject
async def move_node(
    node_id: UUID,
    data: MoveNodeCommand,
    uc: Annotated[MoveNodeUseCase, Depends(Provide["roadmap.move_node_use_case"])],
):
    await uc.invoke(node_id, data)
