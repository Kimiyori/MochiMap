from core.config.base import BaseSettings


class ApplicationSettings(BaseSettings):
    PROJECT_NAME: str = "Mochi Map API"
    VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
