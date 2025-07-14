from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.infrastructure.adapters.keycloak import KeycloakClient


class AuthService:
    security = HTTPBearer()

    def __init__(self, keycloak_client: KeycloakClient):
        self.keycloak_client = keycloak_client

    async def get_current_user(self, credentials: Annotated[HTTPAuthorizationCredentials, Security(security)]) -> dict:
        """Get the current user from a validated token."""
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = credentials.credentials
        token_data = await self.keycloak_client.validate_token(token)
        return token_data

    async def get_current_active_user(self, current_user: dict = None) -> dict:
        """Get the current active user."""
        if current_user is None:
            current_user = await self.get_current_user()
        # You can add additional checks here, like if the user is disabled
        return current_user

    async def has_role(self, required_role: str, current_user: dict = None) -> dict:
        """Check if a user has a specific role."""
        if current_user is None:
            current_user = await self.get_current_user()

        roles = current_user.get("realm_access", {}).get("roles", [])
        if required_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} is required",
            )
        return current_user

    def get_user_id(self, current_user: dict) -> UUID:
        """Extract and convert the user ID from the Keycloak user data."""
        return UUID(current_user.get("sub"))

    async def get_login_url(self, redirect_uri: str) -> str:
        """Get the login URL for redirecting to Keycloak."""
        return await self.keycloak_client.get_login_url(redirect_uri)

    async def exchange_code(self, code: str, redirect_uri: str) -> dict:
        """Exchange an authorization code for tokens."""
        return await self.keycloak_client.exchange_code(code, redirect_uri)

    async def refresh_token(self, refresh_token: str) -> dict:
        """Refresh an access token using a refresh token."""
        return await self.keycloak_client.refresh_token(refresh_token)

    async def logout(self, refresh_token: str) -> None:
        """Logout a user by invalidating their refresh token."""
        return await self.keycloak_client.logout(refresh_token)
