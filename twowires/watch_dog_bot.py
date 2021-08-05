import signal
from asyncio import ensure_future, get_event_loop, sleep
from enum import Enum, auto, unique
from logging import getLogger
from typing import Callable, Optional

from twowires.commands import Commands
from twowires.events import Events
from twowires.messages import Messages
from twowires.telegram_bot_api import TelegramBotApi

logger = getLogger(__name__)


@unique
class BotEvent(Enum):
    STARTUP = auto()
    SHUTDOWN = auto()
    ON_MESSAGE = auto()


class Managers(Enum):
    COMMAND = Commands()
    MESSAGE = Messages()
    EVENT = Events()


class WatchDogBot:
    def __init__(
        self,
        token: str,
    ) -> None:
        super().__init__()
        self.api = TelegramBotApi(token)

    def __getattr__(
        self,
        name: str,
    ) -> Callable:
        for manager in Managers:
            suffix = manager.name.lower()
            if name == f"on_{suffix}":
                return manager.value.decorator
            if name == f"add_{suffix}_handler":
                return manager.value.add_handler
            if name == f"check_{suffix}_handlers":
                return manager.value.check_handlers
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    async def _loop(self) -> None:
        offset: Optional[int] = None
        while True:
            updates, latest_update_id = await self.api.get_updates(timeout=60, offset=offset)
            if updates:
                for update in updates:
                    try:
                        await self.check_event_handlers(BotEvent.ON_MESSAGE, message=update.message)
                        await self.check_command_handlers(update.message)
                        await self.check_message_handlers(update.message)
                    except Exception as err:  # noqa, pylint: disable=broad-except
                        logger.error(err)
                offset = latest_update_id + 1
            await sleep(1)

    async def _close(self) -> None:
        await self.check_event_handlers(BotEvent.SHUTDOWN)

    async def serve(self) -> None:
        loop = get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, callback=lambda: ensure_future(self._close()))
            except NotImplementedError:
                break
        await self.check_event_handlers(BotEvent.STARTUP)
        await self._loop()
