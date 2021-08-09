from abc import ABCMeta
from typing import Any

from pydantic import BaseSettings

from chatushka.transports.telegram_bot_api import TelegramBotApi


async def check_preconditions(
    api: TelegramBotApi,
) -> None:
    response = await api.get_me()
    if not response.can_join_groups:
        raise RuntimeError("Talk to @botfather and enable groups access for bot.")
    if not response.can_read_all_group_messages:
        raise RuntimeError("Talk to @botfather and disable the privacy mode.")


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
