from functools import lru_cache
from typing import Union

from pydantic import BaseSettings

SETTINGS_ENV_PREFIX = "bot_"


class _Settings(BaseSettings):
    token: str
    debug: bool = False
    command_prefixes: Union[str, tuple[str, ...]] = (
        "/",
        "!",
    )
    command_postfixes: Union[str, tuple[str, ...]] = (
        "!",
    )
    allow_raw_command: bool = True

    class Config:
        env_prefix = SETTINGS_ENV_PREFIX
        env_file = ".env"
        allow_mutation = False


@lru_cache
def get_settings() -> _Settings:
    return _Settings()
