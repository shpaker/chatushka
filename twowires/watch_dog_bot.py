import signal
from asyncio import ensure_future, get_event_loop, sleep
from logging import getLogger
from typing import Callable, Optional

from twowires.matchers import (
    CommandsMatcher,
    EventsMatcher,
    RegexMatcher,
    MatcherProtocol,
    BotEvents,
)
from twowires.transports.telegram_bot_api import TelegramBotApi

logger = getLogger(__name__)


class WatchDogBot:
    def __init__(
        self,
        token: str,
    ) -> None:
        super().__init__()
        self.api = TelegramBotApi(token)
        self.matchers: dict[str, MatcherProtocol] = dict(
            events=EventsMatcher(),
            commands=CommandsMatcher(),
            regex=RegexMatcher(),
        )

    def __getattr__(
        self,
        name: str,
    ) -> Callable:
        for suffix, matcher in self.matchers.items():
            if name == f"on_{suffix}":
                return matcher.decorator
            if name == f"add_{suffix}_handler":
                return matcher.add_handler
            if name == f"check_{suffix}_handlers":
                return matcher.check_handlers
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    async def _loop(self) -> None:
        offset: Optional[int] = None
        while True:
            updates, latest_update_id = await self.api.get_updates(timeout=60, offset=offset)
            if updates:
                for update in updates:
                    try:
                        for matcher in self.matchers.values():
                            await matcher.match(update.message)
                    except Exception as err:  # noqa, pylint: disable=broad-except
                        logger.error(err)
                offset = latest_update_id + 1
            await sleep(1)

    async def _close(self) -> None:
        events_matcher = self.matchers["event"]
        await events_matcher.call(BotEvents.SHUTDOWN)

    async def serve(self) -> None:
        loop = get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, callback=lambda: ensure_future(self._close()))
            except NotImplementedError:
                break
        events_matcher = self.matchers["event"]
        await events_matcher.call(BotEvents.two_wires)
        await self._loop()
