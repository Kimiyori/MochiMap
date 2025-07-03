from common.protocols.use_case import BaseUseCase
from infrastructure.adapters.keycloak import KeycloakClient
from infrastructure.persistence.transaction.transaction import async_transactional
from infrastructure.persistence.transaction.unit_of_work import SqlAlchemyUnitOfWork


class AuthUseCase(BaseUseCase):
    def __init__(self, uow: SqlAlchemyUnitOfWork, keycloak: KeycloakClient) -> None:
        self.uow = uow
        self.keycloak = keycloak

    @async_transactional()
    async def invoke(self, keycode: str) -> None:
        token = self.keycloak.client.token(
            grant_type="authorization_code",
            code=keycode,
            redirect_uri="http://localhost:8000/api/auth/auth",
            scope="openid profile email",
        )
        return token
