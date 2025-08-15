from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.infrastructure.dependencies.app_container import AppContainer  # noqa: F401
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.get_all_roadmaps.impl import GetUserRoadmapsUseCase
from src.modules.roadmap.use_cases.get_all_roadmaps.response_dto import RoadmapResponseDTO


@roadmap_router.get(
    path="", name="Get User Roadmaps", status_code=status.HTTP_200_OK, response_model=list[RoadmapResponseDTO]
)
@inject
async def get_user_roadmaps(
    uc: Annotated[GetUserRoadmapsUseCase, Depends(Provide["roadmap.get_user_roadmaps_use_case"])],
):
    return await uc.invoke()
