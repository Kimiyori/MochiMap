from collections.abc import Iterable
from typing import Any

from src.common.errors import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    InternalServerException,
    NotFoundException,
    UnauthorizedException,
    UnsupportedMediaTypeException,
)
from src.common.pydantic import BaseErrorResponse

# Mapping of known HTTP-style exceptions to their default status codes and short descriptions.
_EXC_TO_SPEC: dict[type[BaseException], tuple[int, str]] = {
    BadRequestException: (400, "Bad Request"),
    UnauthorizedException: (401, "Unauthorized"),
    ForbiddenException: (403, "Forbidden"),
    NotFoundException: (404, "Not Found"),
    ConflictException: (409, "Conflict"),
    UnsupportedMediaTypeException: (415, "Unsupported Media Type"),
    InternalServerException: (500, "Internal Server Error"),
}


def error_responses(
    *exceptions: type[BaseException] | Iterable[type[BaseException]],
    include_unexpected_500: bool = True,
) -> dict[int, dict[str, Any]]:
    """
    Build a FastAPI-compatible "responses" mapping for OpenAPI based on exception classes.

    - Each provided exception class is mapped to a status code and a JSON schema of BaseErrorResponse.
    - Optionally appends a generic 500 response for unexpected errors.
    """
    items: list[type[BaseException]] = []
    for exc in exceptions:
        if isinstance(exc, Iterable):
            items.extend(list(exc))
        else:
            items.append(exc)

    responses: dict[int, dict[str, Any]] = {}
    for exc_type in items:
        spec = _EXC_TO_SPEC.get(exc_type)
        if not spec:
            continue
        status_code, description = spec
        responses[status_code] = {
            "description": description,
            "model": BaseErrorResponse,
        }

    if include_unexpected_500 and 500 not in responses:
        responses[500] = {
            "description": "Internal Server Error",
            "model": BaseErrorResponse,
        }

    return responses
