from abc import ABCMeta
from typing import Any

from pydantic import BaseSettings


class ServiceSettingsBase(BaseSettings):
    class Config:
        env_prefix = "BOT_"
        env_file = ".env"
        allow_mutation = False


class SingletonABCMeta(ABCMeta):
    _instances = {}  # type: ignore

    def __call__(cls, *args: Any, **kwargs: Any):  # type: ignore
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonABCMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
