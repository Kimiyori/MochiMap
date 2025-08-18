from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.common.domain_errors import BaseDomainError
from src.common.errors import BaseHttpException
from src.common.pydantic import BaseErrorResponse


def register_error_handling(app: FastAPI) -> None:
    @app.exception_handler(BaseDomainError)
    async def handle_domain_error(_: Request, exc: BaseDomainError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content=BaseErrorResponse(
                message=str(exc) or exc.__class__.__name__,
                error=exc.__class__.__name__,
            ).model_dump(),
        )

    @app.exception_handler(BaseHttpException)
    async def handle_application_error(_: Request, exc: BaseHttpException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=BaseErrorResponse(
                message=str(exc) or exc.__class__.__name__,
                error=exc.__class__.__name__,
            ).model_dump(),
        )
