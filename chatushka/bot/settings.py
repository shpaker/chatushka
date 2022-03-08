from functools import lru_cache
from typing import Union

from pydantic import BaseModel

from chatushka.core.utils import ServiceSettingsBase


class HeroesCollectionsSettings(BaseModel):
    calendar_collection: str = "heroes_calendar"
    activations_collection: str = "heroes_activations"


class MongoDBSubSettings(BaseModel):
    database: str = "chatushka"
    heroes: HeroesCollectionsSettings = HeroesCollectionsSettings()


class _Settings(ServiceSettingsBase):
    command_prefixes: Union[str, tuple[str, ...]] = ("/", "!")
    command_postfixes: Union[str, tuple[str, ...]] = "!"


@lru_cache
def get_settings() -> _Settings:
    return _Settings()
