from asyncio import iscoroutinefunction
from logging import getLogger
from re import findall as re_find_all
from typing import Callable, Coroutine, List, Union

from twowires import models
from twowires.protocols import Manager

logger = getLogger(__name__)


class Messages(Manager):
    def __init__(
        self,
    ) -> None:
        self.messages_handlers: dict[
            str,
            list[Union[Callable[[models.Message, List[str]], None], Callable[[models.Message, List[str]], Coroutine]]],
        ] = dict()

    def decorator(
        self,
        regex: str,
    ) -> Callable[[Callable[[], None]], None]:
        def decorator(
            func: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
        ) -> None:
            self.add_handler(regex=regex, handler=func)

        return decorator

    def add_handler(
        self,
        regex: str,
        handler: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
    ) -> None:
        if regex not in self.messages_handlers:
            self.messages_handlers[regex] = list()
        self.messages_handlers[regex].append(handler)  # type: ignore

    async def check_handlers(
        self,
        message: models.Message,
    ) -> None:
        for regex, funcs in self.messages_handlers.items():
            if founded := re_find_all(regex, message.text):
                for func in funcs:
                    if iscoroutinefunction(func):
                        await func(message, founded)  # type: ignore
                        continue
                    func(message, founded)
