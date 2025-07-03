from core.config.application import ApplicationSettings
from core.config.auth import AuthSettings
from core.config.db import DatabaseSettings

APP_SETTINGS = ApplicationSettings()
AUTH_SETTINGS = AuthSettings()
DB_SETTINGS = DatabaseSettings()


__all__ = [
    "APP_SETTINGS",
    "AUTH_SETTINGS",
    "DB_SETTINGS",
]
