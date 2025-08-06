from uuid import UUID

from pydantic import BaseModel


class CreateNewNodeResponseDTO(BaseModel):
    id: UUID
