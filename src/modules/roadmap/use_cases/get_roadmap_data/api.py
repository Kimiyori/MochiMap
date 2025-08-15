from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.common.errors import NotFoundException
from src.common.openapi import error_responses
from src.infrastructure.dependencies.app_container import AppContainer  # noqa: F401
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.get_roadmap_data.impl import GetRoadmapDataUseCase
from src.modules.roadmap.use_cases.get_roadmap_data.response_dto import (
    GetRoadmapDataResponseDTO,
)


@roadmap_router.get(
    path="/{roadmap_id:uuid}/data",
    name="Get Roadmap Data",
    status_code=status.HTTP_200_OK,
    response_model=GetRoadmapDataResponseDTO,
    responses=error_responses(NotFoundException),
    description=(
        "Get a roadmap with its nodes and edges.\n\n"
        "Status codes:\n"
        "- 200: OK\n"
        "- 404: Roadmap not found\n"
        "- 500: Internal Server Error"
    ),
)
@inject
async def get_roadmap_data(
    roadmap_id: UUID,
    uc: Annotated[GetRoadmapDataUseCase, Depends(Provide["roadmap.get_roadmap_nodes_use_case"])],
):
    return await uc.invoke(roadmap_id)
