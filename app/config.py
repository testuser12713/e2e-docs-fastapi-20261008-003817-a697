"""Application configuration, loaded from the environment via pydantic-settings.

Both fields carry a default, so the service boots with no environment variable
set. Environment variable names are the field names upper-cased:
``APP_NAME`` and ``LOG_LEVEL``.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the notes service."""

    model_config = SettingsConfigDict(case_sensitive=False)

    app_name: str = "Notes API"
    log_level: str = "INFO"


settings = Settings()
