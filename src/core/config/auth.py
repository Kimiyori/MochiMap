from core.config.base import BaseSettings


class AuthSettings(BaseSettings):
    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    KEYCLOAK_REALM_NAME: str
