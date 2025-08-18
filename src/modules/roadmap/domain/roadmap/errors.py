from typing import ClassVar

from src.common.domain_errors import BaseDomainError


class RoadmapValidationError(BaseDomainError):
    ERROR_MAP: ClassVar[dict[str, str]] = {"title": "Title must not be empty."}

    def __init__(self, keys: list[str]):
        self.keys = keys
        self.errors = {key: self.ERROR_MAP.get(key, "Invalid value.") for key in keys}
        message = "Roadmap validation error(s): " + ", ".join(f"{k}: {v}" for k, v in self.errors.items())
        super().__init__(message)
