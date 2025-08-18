from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.common.openapi import error_responses
from src.infrastructure.dependencies.app_container import AppContainer  # noqa: F401
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.get_all_roadmaps.impl import GetUserRoadmapsUseCase
from src.modules.roadmap.use_cases.get_all_roadmaps.response_dto import RoadmapResponseDTO


@roadmap_router.get(
    path="",
    name="Get User Roadmaps",
    status_code=status.HTTP_200_OK,
    response_model=list[RoadmapResponseDTO],
    responses=error_responses(),
    description=("Get all roadmaps for the current user.\n\nStatus codes:\n- 200: OK\n- 500: Internal Server Error"),
)
@inject
async def get_user_roadmaps(
    uc: Annotated[GetUserRoadmapsUseCase, Depends(Provide["roadmap.get_user_roadmaps_use_case"])],
):
    return await uc.invoke()
