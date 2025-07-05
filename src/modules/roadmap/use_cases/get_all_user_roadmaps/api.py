
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.dependencies.container import Container
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.get_all_user_roadmaps.impl import GetUserRoadmapsUseCase


@roadmap_router.get(path="/{owned_id}", name="Get User Roadmaps", status_code=status.HTTP_200_OK)
@inject
async def get_user_roadmaps(
    owned_id: str,
    uc: Annotated[GetUserRoadmapsUseCase, Depends(Provide[Container.get_user_roadmaps_use_case])],
):
    return await uc.invoke(owned_id)
