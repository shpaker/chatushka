from functools import lru_cache
from pathlib import Path
from typing import Union

from chatushka.core.utils import ServiceSettingsBase

BOBUK_JOKES_URL = "https://jokesrv.rubedo.cloud/"

BOT_ROOT_DIR = Path(__file__).parent.resolve()
BOT_DATA_DIR = BOT_ROOT_DIR / "data"


class _Settings(ServiceSettingsBase):
    command_prefixes: Union[str, tuple[str, ...]] = ("/", "!")
    command_postfixes: Union[str, tuple[str, ...]] = "!"


@lru_cache
def get_settings() -> _Settings:
    return _Settings()
