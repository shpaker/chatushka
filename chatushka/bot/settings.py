from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

BOBUK_JOKES_URL = "https://jokesrv.rubedo.cloud/"
BOT_ROOT_DIR = Path(__file__).parent.resolve()
BOT_DATA_DIR = BOT_ROOT_DIR / "data"


class _Settings(BaseSettings):
    command_prefixes: str | tuple[str, ...] = ("/", "!")
    command_postfixes: str | tuple[str, ...] = "!"

    class Config:
        env_prefix = "BOT_"
        env_file = ".env"
        allow_mutation = False


@lru_cache
def get_settings() -> _Settings:
    return _Settings()
