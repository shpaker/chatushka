from functools import lru_cache
from typing import Union

from pydantic import BaseModel

from chatushka.samples.matchers.heroes.settings import HeroesSettings
from chatushka.utils import ServiceSettingsBase


class SamplesSubSettings(BaseModel):
    heroes: HeroesSettings = HeroesSettings()


class MongoDBSubSettings(BaseModel):
    database: str = "chatushka"


class PaginationSubSettings(BaseModel):
    per_page_default: int = 16
    per_page_maximum: int = 64


class _Settings(ServiceSettingsBase):
    token: str
    debug: bool = False
    command_prefixes: Union[str, tuple[str, ...]] = ("/", "!")
    command_postfixes: Union[str, tuple[str, ...]] = "!"
    allow_raw_command: bool = True
    mongodb: MongoDBSubSettings = MongoDBSubSettings()
    pagination: PaginationSubSettings = PaginationSubSettings()
    samples: SamplesSubSettings = SamplesSubSettings()


@lru_cache
def get_settings() -> _Settings:
    return _Settings()
