from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from inspect import iscoroutinefunction, signature
from random import random
from re import Pattern, compile
from typing import TypeVar

from chatushka._models import Update
from chatushka._transport import TelegramBotAPI

Matcher = TypeVar("Matcher", bound="BaseMatcher")


class BaseMatcher(
    ABC,
):
    def __init__(
        self,
        action: Callable,
        chance_rate: float = 1.0,
    ) -> None:
        self._action: Callable = action
        self._chance_rate = chance_rate

    @abstractmethod
    def _check(
        self,
        update: Update,
    ) -> bool:
        raise NotImplementedError

    async def __call__(
        self,
        api: TelegramBotAPI,
        update: Update,
    ) -> None:
        if not self._check(
            update=update,
        ):
            return
        await self._call_action(
            api=api,
            update=update,
        )

    def _get_chance(
        self,
    ) -> bool:
        return random() <= self._chance_rate

    async def _call_action(
        self,
        api: TelegramBotAPI,
        update: Update,
    ) -> None:
        if not self._get_chance():
            return
        kwargs = {}
        kwargs.update(
            {
                "api": api,
                "update": update,
                "message": update.message,
                "chat": update.message.chat if update.message else None,
                "user": update.message.user if update.message else None,
            }
        )
        sig = signature(self._action)
        kwargs = {param: kwargs.get(param) for param in sig.parameters if param in kwargs}
        if update and update.message is not None and "message" in sig.parameters:
            kwargs["message"] = update.message
        if iscoroutinefunction(self._action):
            await self._action(**kwargs)
            return
        self._action(**kwargs)


class CommandMatcher(
    BaseMatcher,
    ABC,
):
    def __init__(
        self,
        *commands: str,
        action: Callable,
        prefixes: str | Sequence[str] = (),
        case_sensitive: bool = False,
        chance_rate: float = 1.0,
    ) -> None:
        super().__init__(
            action=action,
            chance_rate=chance_rate,
        )
        if case_sensitive:
            commands = tuple(command.upper() for command in commands)
        self._commands = commands
        self._case_sensitive = case_sensitive
        if prefixes:
            self.add_commands_prefixes(prefixes)

    def add_commands_prefixes(
        self,
        prefixes: Sequence[str],
    ) -> None:
        if not prefixes:
            return
        self._commands = tuple(f"{prefix}{command}" for command in self._commands for prefix in prefixes)

    def _check(
        self,
        update: Update,
    ) -> bool:
        if not update.message or not update.message.text:
            return False
        case_sensitive = self._case_sensitive or False
        for command in self._commands:
            if case_sensitive and update.message.text.upper().startswith(command.upper()):
                return True
            if update.message.text.startswith(command):
                return True
        return False


class RegExMatcher(
    BaseMatcher,
    ABC,
):
    def __init__(
        self,
        *patterns: str | Pattern,
        action: Callable,
        chance_rate: float = 1.0,
    ) -> None:
        super().__init__(
            action=action,
            chance_rate=chance_rate,
        )
        self._patterns = [compile(pattern) if isinstance(pattern, str) else pattern for pattern in patterns]

    def _check(
        self,
        update: Update,
    ) -> bool:
        if not update.message or not update.message.text:
            return False
        return any(pattern.findall(update.message.text) for pattern in self._patterns)
