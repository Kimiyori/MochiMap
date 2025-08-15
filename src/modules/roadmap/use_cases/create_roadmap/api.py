from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.infrastructure.dependencies.app_container import AppContainer  # noqa: F401
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.create_roadmap.command import CreateRoadmapCommand
from src.modules.roadmap.use_cases.create_roadmap.impl import CreateRoadmapUseCase


@roadmap_router.post(path="/", name="Create New Roadmap", status_code=status.HTTP_201_CREATED)
@inject
async def create_new_roadmap(
    data: CreateRoadmapCommand,
    uc: Annotated[CreateRoadmapUseCase, Depends(Provide["roadmap.create_roadmap_use_case"])],
):
    return await uc.invoke(data)
