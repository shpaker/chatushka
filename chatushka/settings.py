from functools import lru_cache
from typing import Union

from pydantic import BaseModel

from chatushka.utils import ServiceSettingsBase


class MongoDBSubSettings(BaseModel):
    database: str = "meowrl"
    homm_collection: str = "homm"


class PaginationSubSettings(BaseModel):
    per_page_default: int = 16
    per_page_maximum: int = 64


class _Settings(ServiceSettingsBase):
    token: str
    debug: bool = False
    command_prefixes: Union[str, tuple[str, ...]] = ("/", "!")
    command_postfixes: Union[str, tuple[str, ...]] = "!"
    allow_raw_command: bool = True
    admins: tuple[int, ...] = (
        514026725,
        147727588,
    )
    mongodb: MongoDBSubSettings = MongoDBSubSettings()
    pagination: PaginationSubSettings = PaginationSubSettings()


@lru_cache
def get_settings() -> _Settings:
    return _Settings()
