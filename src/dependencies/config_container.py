from dependency_injector import containers
from dependency_injector.providers import Configuration

from core.config import APP_SETTINGS, AUTH_SETTINGS, DB_SETTINGS


class ConfigContainer(containers.DeclarativeContainer):
    app_config = Configuration()
    auth_config = Configuration()
    db_config = Configuration()
    # Load settings
    app_config.from_pydantic(APP_SETTINGS)
    auth_config.from_pydantic(AUTH_SETTINGS)
    db_config.from_pydantic(DB_SETTINGS)
