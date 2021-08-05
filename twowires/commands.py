from asyncio import iscoroutinefunction
from logging import getLogger
from typing import Callable, Coroutine, Iterable, Union

from twowires import models
from twowires.protocols import Manager
from twowires.settings import get_settings

logger = getLogger(__name__)

settings = get_settings()


class Commands(Manager):
    def __init__(
        self,
    ) -> None:
        command_prefixes = settings.command_prefixes
        command_postfixes = settings.command_postfixes
        if isinstance(command_prefixes, str):
            command_prefixes = (command_prefixes,)
        if isinstance(command_postfixes, str):
            command_prefixes = (command_prefixes,)
        command_variations = [prefix + "{cmd}" for prefix in command_prefixes if prefix.strip()] + [
            "{cmd}" + postfix for postfix in command_postfixes if postfix.strip()
        ]
        if settings.allow_raw_command:
            command_variations.append("{cmd}")
        self.command_variations = set(command_variations)
        self.command_handlers: dict[  # type: ignore
            str,
            list[Union[Callable[[models.Message], None], Callable[[models.Message], Coroutine]]],
        ] = dict()

    def decorator(
        self,
        *commands: str,
    ) -> Callable[[Callable[[], None]], None]:
        def decorator(
            func: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
        ) -> None:
            self.add_handler(tokens=commands, handler=func)

        return decorator

    def add_handler(
        self,
        tokens: Union[str, Iterable[str]],
        handler: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
    ) -> None:
        for command in tokens:
            command = command.strip()
            if command not in self.command_handlers:
                self.command_handlers[command] = list()
            self.command_handlers[command].append(handler)  # type: ignore

    async def check_handlers(
        self,
        message: models.Message,
    ) -> None:

        for command, funcs in self.command_handlers.items():
            for variation in self.command_variations:
                message_words = message.text.lower().strip().split(" ")
                if variation.format(cmd=command).lower() in message_words:
                    for func in funcs:
                        if iscoroutinefunction(func):
                            await func(message)  # type: ignore
                            continue
                        func(message)
