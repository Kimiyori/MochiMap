from http.client import HTTPException

from fastapi import HTTPException, status
from keycloak import KeycloakOpenID

from src.core.config.auth import AuthSettings


class KeycloakClient:
    def __init__(self, auth_config: AuthSettings) -> None:
        self.keycloak_openid = KeycloakOpenID(
            server_url=auth_config["KEYCLOAK_SERVER_URL"],
            client_id=auth_config["KEYCLOAK_CLIENT_ID"],
            realm_name=auth_config["KEYCLOAK_REALM_NAME"],
            client_secret_key=auth_config["KEYCLOAK_CLIENT_SECRET"],
            verify=False,
        )
        self._public_key = None
        self._init_public_key()

    @property
    def client(self):
        return self.keycloak_openid
        
    def _init_public_key(self):
        """Initialize the public key for token validation."""
        keys_response = self.keycloak_openid.public_key()
        self._public_key = f"-----BEGIN PUBLIC KEY-----\n{keys_response}\n-----END PUBLIC KEY-----"

    async def validate_token(self, token: str) -> dict:
        """Validate an access token and return the decoded payload."""
        try:
            options = {"verify_signature": True, "verify_aud": False, "verify_exp": True}
            return self.keycloak_openid.decode_token(token, key=self._public_key, options=options)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {e!s}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_user_info(self, token: str) -> dict:
        """Get user info from Keycloak using the token."""
        return self.keycloak_openid.userinfo(token)
        
    async def get_openid_config(self):
        """Get the OpenID configuration from Keycloak."""
        return await self.keycloak_openid.a_well_known()

    async def get_login_url(self, redirect_uri: str) -> str:
        """Get the login URL for redirecting to Keycloak."""
        return await self.keycloak_openid.a_auth_url(redirect_uri)
        
    async def exchange_code(self, code: str, redirect_uri: str) -> dict:
        """Exchange an authorization code for tokens."""
        return self.keycloak_openid.token(
            grant_type=["authorization_code"],
            code=code,
            redirect_uri=redirect_uri
        )
        
    async def refresh_token(self, refresh_token: str) -> dict:
        """Refresh an access token using a refresh token."""
        return self.keycloak_openid.refresh_token(refresh_token)
        
    async def logout(self, refresh_token: str) -> None:
        """Logout a user by invalidating their refresh token."""
        return self.keycloak_openid.logout(refresh_token)