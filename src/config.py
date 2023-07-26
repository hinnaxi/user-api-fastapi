from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any
from src.constants import Environment


class Settings(BaseSettings):
    APP_VERSION: str
    APP_NAME: str
    APP_DOMAIN: str
    APP_SERVERS: list[dict[str, str]]
    ENVIRONMENT: Environment = Environment.TESTING
    DATABASE_URL: str
    CORS_ORIGINS: list[str]
    CORS_HEADERS: list[str]
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXP_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
app_configs: dict[str, Any] = {"servers": settings.APP_SERVERS}

# Hide docs if not debug environment
if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None
