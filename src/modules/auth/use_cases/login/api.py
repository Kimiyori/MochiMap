from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status
from fastapi.responses import RedirectResponse

from dependencies.container import Container
from modules.auth.use_cases import auth_router
from modules.auth.use_cases.login.impl import RegistrationUseCase


@auth_router.get(path="/login", name="New Author", status_code=status.HTTP_201_CREATED)
@inject
async def new_author(
    uc: Annotated[RegistrationUseCase, Depends(Provide[Container.registration_use_case])],
):
    auth_url = await uc.invoke()
    return RedirectResponse(auth_url)
