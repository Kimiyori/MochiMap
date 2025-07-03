from common.protocols.use_case import BaseUseCase
from infrastructure.adapters.keycloak import KeycloakClient
from infrastructure.persistence.transaction.transaction import async_transactional
from infrastructure.persistence.transaction.unit_of_work import SqlAlchemyUnitOfWork


class RegistrationUseCase(BaseUseCase):
    def __init__(self, uow: SqlAlchemyUnitOfWork, keycloak: KeycloakClient) -> None:
        self.uow = uow
        self.keycloak = keycloak

    @async_transactional()
    async def invoke(self):
        return await self.keycloak.client.a_auth_url(
            redirect_uri="http://localhost:8000/api/auth/auth", scope="openid profile email"
        )
