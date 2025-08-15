from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.infrastructure.dependencies.app_container import AppContainer  # noqa: F401
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.delete_edge.impl import DeleteEdgeUseCase


@roadmap_router.delete(
    path="/edge/{edge_id:uuid}",
    name="Delete edge",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_edge(
    edge_id: UUID,
    uc: Annotated[DeleteEdgeUseCase, Depends(Provide["roadmap.delete_edge_use_case"])],
):
    await uc.invoke(edge_id)
