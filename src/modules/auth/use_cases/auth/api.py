
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request, status

from dependencies.container import Container
from modules.auth.use_cases import auth_router
from modules.auth.use_cases.auth.impl import AuthUseCase


@auth_router.get(path="/auth", name="New Author", status_code=status.HTTP_201_CREATED)
@inject
async def new_author(
    request: Request,
     uc: Annotated[AuthUseCase, Depends(Provide[Container.auth_use_case])],
):
    keycode = request.query_params.get('code')
    return await uc.invoke(keycode=keycode)