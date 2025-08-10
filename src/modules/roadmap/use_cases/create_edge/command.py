from uuid import UUID

from src.common.pydantic import BaseRequestCommand


class CreateEdgeCommand(BaseRequestCommand):
    source_id: UUID
    target_id: UUID

class CreateEdgeResponseDTO(BaseRequestCommand):
    id: UUID
