from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.common.errors import NotFoundException
from src.common.openapi import error_responses
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.delete_node.impl import DeleteNodeUseCase


@roadmap_router.delete(
    path="/node/{node_id:uuid}",
    name="Delete node",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=error_responses(NotFoundException),
)
@inject
async def delete_node(
    node_id: UUID,
    uc: Annotated[DeleteNodeUseCase, Depends(Provide["roadmap.delete_node_use_case"])],
):
    await uc.invoke(node_id)
