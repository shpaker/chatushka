import signal
from asyncio import ensure_future, get_event_loop, iscoroutinefunction, sleep
from enum import Enum, auto, unique
from logging import getLogger
from re import search as re_search
from typing import Any, Callable, Coroutine, Optional, Union

from twowires.models import telegram_types
from twowires.telegram import get_updates

logger = getLogger(__name__)


@unique
class BotEvent(Enum):
    STARTUP = auto()
    SHUTDOWN = auto()
    ON_MESSAGE = auto()


class TwoWiresBot:
    def __init__(self) -> None:
        self.events_handlers: dict[  # type: ignore
            BotEvent,
            list[Union[Callable[[...], None], Callable[[...], Coroutine]]],
        ] = dict()
        self.messages_handlers: dict[  # type: ignore
            str,
            list[Union[Callable[[telegram_types.Message], None], Callable[[telegram_types.Message], Coroutine]]],
        ] = dict()

    def on_event(
        self,
        event: Union[BotEvent, str],
    ) -> Callable[[Callable[[], None]], None]:
        def decorator(
            func: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
        ) -> None:
            self.add_event_handler(event=event, handler=func)

        return decorator

    def on_message(
        self,
        regex: str,
    ) -> Callable[[Callable[[], None]], None]:
        def decorator(
            func: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
        ) -> None:
            self.add_message_handler(regex=regex, handler=func)

        return decorator

    def add_event_handler(
        self,
        event: Union[BotEvent, str],
        handler: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
    ) -> None:
        if isinstance(event, str):
            event = BotEvent[event.upper()]
        if event not in self.events_handlers:
            self.events_handlers[event] = list()
        self.events_handlers[event].append(handler)  # type: ignore

    def add_message_handler(
        self,
        regex: str,
        handler: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
    ) -> None:
        if regex not in self.messages_handlers:
            self.messages_handlers[regex] = list()
        self.messages_handlers[regex].append(handler)  # type: ignore

    async def _loop(self) -> None:
        offset: Optional[int] = None
        while True:
            updates, latest_update_id = await get_updates(timeout=60, offset=offset)
            if updates:
                for update in updates:
                    await self._call_event_handlers(BotEvent.ON_MESSAGE, message=update.message)
                    await self._call_message_handlers(update.message)
                offset = latest_update_id + 1
            await sleep(1)

    async def _close(self) -> None:
        await self._call_event_handlers(BotEvent.SHUTDOWN)

    async def _call_event_handlers(
        self,
        event: BotEvent,
        **kwargs: Any,
    ) -> None:
        handlers = self.events_handlers.get(event, list())
        for handler in handlers:
            if iscoroutinefunction(handler):
                await handler(**kwargs)  # type: ignore
                continue
            handler(**kwargs)  # type: ignore

    async def _call_message_handlers(
        self,
        message: telegram_types.Message,
    ) -> None:
        for regex, funcs in self.messages_handlers.items():
            if re_search(regex, message.text):
                for func in funcs:
                    if iscoroutinefunction(func):
                        await func(message)  # type: ignore
                        continue
                    func(message)

    async def serve(self) -> None:
        loop = get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, callback=lambda: ensure_future(self._close()))
            except NotImplementedError:
                break
        await self._call_event_handlers(BotEvent.STARTUP)
        await self._loop()
