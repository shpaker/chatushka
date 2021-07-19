from functools import lru_cache

from pydantic import BaseSettings

SETTINGS_ENV_PREFIX = "bot_"


class _Settings(BaseSettings):
    token: str
    debug: bool = False

    class Config:
        env_prefix = SETTINGS_ENV_PREFIX
        env_file = ".env"
        allow_mutation = False


@lru_cache
def get_settings() -> _Settings:
    return _Settings()
