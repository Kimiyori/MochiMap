from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request

from src.dependencies.container import Container
from src.modules.security.infrastructure.auth_service import AuthService
from src.modules.security.use_cases import auth_router


@auth_router.get("/login")
@inject
async def login(
    request: Request,
    auth_service: Annotated[AuthService, Depends(Provide[Container.infrastructure.auth_service])]
):
    """Get login URL for Keycloak authentication."""
    redirect_uri = request.url_for("auth")
    login_url = await auth_service.get_login_url(str(redirect_uri))
    return {"login_url": login_url}

@auth_router.get("/auth")
@inject
async def auth(
    code: str,
    request: Request,
    auth_service: Annotated[AuthService, Depends(Provide[Container.infrastructure.auth_service])]
):
    """Handle the callback from Keycloak authentication."""
    redirect_uri = request.url_for("auth")
    tokens = await auth_service.exchange_code(code, str(redirect_uri))
    return tokens