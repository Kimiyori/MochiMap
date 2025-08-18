from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.common.errors import NotFoundException
from src.common.openapi import error_responses
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.delete_edge.impl import DeleteEdgeUseCase


@roadmap_router.delete(
    path="/edge/{edge_id:uuid}",
    name="Delete edge",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=error_responses(NotFoundException),
)
@inject
async def delete_edge(
    edge_id: UUID,
    uc: Annotated[DeleteEdgeUseCase, Depends(Provide["roadmap.delete_edge_use_case"])],
):
    await uc.invoke(edge_id)
