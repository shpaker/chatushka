from asyncio import iscoroutinefunction
from enum import Enum, auto, unique
from logging import getLogger
from typing import Any, Callable, Coroutine, Union

from twowires.protocols import Manager

logger = getLogger(__name__)


@unique
class BotEvent(Enum):
    STARTUP = auto()
    SHUTDOWN = auto()
    ON_MESSAGE = auto()


class Events(Manager):

    events_handlers: dict[  # type: ignore
        BotEvent,
        list[Union[Callable[[...], None], Callable[[...], Coroutine]]],
    ] = dict()

    def decorator(
        self,
        event: Union[BotEvent, str],
    ) -> Callable[[Callable[[], None]], None]:
        def decorator(
            func: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
        ) -> None:
            self.add_handler(event=event, handler=func)

        return decorator

    def add_handler(
        self,
        event: Union[BotEvent, str],
        handler: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
    ) -> None:
        if isinstance(event, str):
            event = BotEvent[event.upper()]
        if event not in self.events_handlers:
            self.events_handlers[event] = list()
        self.events_handlers[event].append(handler)  # type: ignore

    async def check_handlers(
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
