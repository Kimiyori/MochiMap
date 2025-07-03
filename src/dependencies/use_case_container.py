from dependency_injector import providers
from dependency_injector.containers import copy

from dependencies.base_container import BaseContainer
from modules.auth.use_cases.auth.impl import AuthUseCase
from modules.auth.use_cases.login.impl import RegistrationUseCase


@copy(BaseContainer)
class UseCaseContainer(BaseContainer):
    # CANDIDATES
    registration_use_case = providers.Factory(
        RegistrationUseCase, uow=BaseContainer.infrastructure.uow, keycloak=BaseContainer.infrastructure.auth
    )
    auth_use_case = providers.Factory(
        AuthUseCase, uow=BaseContainer.infrastructure.uow, keycloak=BaseContainer.infrastructure.auth
    )
