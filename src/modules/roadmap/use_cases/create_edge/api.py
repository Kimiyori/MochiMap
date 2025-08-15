from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from src.common.errors import BadRequestException, ConflictException, NotFoundException
from src.common.openapi import error_responses
from src.modules.roadmap.use_cases import roadmap_router
from src.modules.roadmap.use_cases.create_edge.command import CreateEdgeCommand, CreateEdgeResponseDTO
from src.modules.roadmap.use_cases.create_edge.impl import CreateEdgeUseCase


@roadmap_router.post(
    path="/{roadmap_id:uuid}/edge",
    name="Create Edge",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateEdgeResponseDTO,
    responses=error_responses([NotFoundException, ConflictException, BadRequestException]),
    description=(
        "Create an edge between two nodes that belong to the specified roadmap.\n\n"
        "Status codes:\n"
        "- 201: Edge created\n"
        "- 400: Invalid edge (domain rules)\n"
        "- 404: Roadmap or nodes not found\n"
        "- 409: Edge already exists\n"
        "- 500: Internal Server Error"
    ),
)
@inject
async def create_edge(
    roadmap_id: UUID,
    data: CreateEdgeCommand,
    uc: Annotated[CreateEdgeUseCase, Depends(Provide["roadmap.create_edge_use_case"])],
):
    return await uc.invoke(roadmap_id, data)
