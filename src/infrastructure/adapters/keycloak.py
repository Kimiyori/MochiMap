from keycloak import KeycloakOpenID

from core.config.auth import AuthSettings


class KeycloakClient:
    def __init__(self, auth_config: AuthSettings) -> None:
        self.keycloak_openid = KeycloakOpenID(
            server_url=auth_config["KEYCLOAK_SERVER_URL"],
            client_id=auth_config["KEYCLOAK_CLIENT_ID"],
            realm_name=auth_config["KEYCLOAK_REALM_NAME"],
            client_secret_key=auth_config["KEYCLOAK_CLIENT_SECRET"],
            verify=False,
        )

    @property
    def client(self):
        return self.keycloak_openid

    async def get_openid_config(self):
        return await self.keycloak_openid.a_well_known()