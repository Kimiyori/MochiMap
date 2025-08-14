from uuid import UUID

from pydantic import Field

from src.common.pydantic import BaseRequestCommand
from src.modules.roadmap.domain.edge.value_objects import EdgeType


class CreateEdgeCommand(BaseRequestCommand):
    source_id: UUID
    target_id: UUID
    type: EdgeType = Field(default=EdgeType.BEZIER)

class CreateEdgeResponseDTO(BaseRequestCommand):
    id: UUID
