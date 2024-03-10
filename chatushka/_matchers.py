from abc import ABC, abstractmethod
from asyncio import gather
from collections.abc import Callable, Coroutine
from inspect import iscoroutinefunction, signature
from re import findall
from typing import Any

from chatushka._models import Update
from chatushka._transport import TelegramBotAPI


class HandlersContainer(
    ABC,
):
    def __init__(
        self,
    ) -> None:
        self._handlers: dict[tuple[str, ...], Any] = {}

    @abstractmethod
    def check_condition(
        self,
        token: str,
        update: Update,
    ) -> bool:
        raise NotImplementedError

    def add_handler(
        self,
        tokens: str | tuple[str, ...],
        handler,
    ) -> None:
        if isinstance(tokens, str):
            tokens = (tokens,)
        self._handlers[tokens] = handler

    @staticmethod
    async def _call_handler(
        handler: Callable,
        api: TelegramBotAPI,
        update: Update,
        **kwargs: Any,
    ) -> None:
        kwargs.update(
            {
                "api": api,
                "update": update,
                "message": update.message,
                "chat": update.message.chat if update.message else None,
                "user": update.message.user if update.message else None,
            }
        )
        sig = signature(handler)
        sig_kwargs = {param: kwargs.get(param) for param in sig.parameters if param in kwargs}
        if update and update.message is not None and "message" in sig.parameters:
            sig_kwargs["message"] = update.message
        (await handler(**sig_kwargs) if iscoroutinefunction(handler) else handler(**sig_kwargs))

    async def check_handlers(
        self,
        api: TelegramBotAPI,
        update: Update,
    ) -> list[Coroutine[Any, Any, None]]:
        handlers_tasks = []
        for tokens, handler in self._handlers.items():
            for token in tokens:
                if self.check_condition(token, update):
                    handlers_tasks.append(
                        self._call_handler(
                            handler,
                            api=api,
                            token=token,
                            update=update,
                        )
                    )
                    break
        return handlers_tasks


class MatchersContainer:
    def __init__(
        self,
    ) -> None:
        self._nested_matchers: list["HandlersContainer"] = []

    def add_matcher(
        self,
        *matchers: "HandlersContainer",
    ) -> None:
        self._nested_matchers += matchers

    async def _check_nested_matchers(
        self,
        api: TelegramBotAPI,
        update: Update,
    ) -> list[Coroutine[Any, Any, None]]:
        handlers_tasks = []
        for matcher in self._nested_matchers:
            handlers_tasks += await matcher.check_handlers(
                api=api,
                update=update,
            )
        return handlers_tasks


class MatcherBase(
    HandlersContainer,
    MatchersContainer,
    ABC,
):
    def __init__(
        self,
    ) -> None:
        super().__init__()
        ...

    def __call__(
        self,
        *tokens: str,
    ) -> Callable[[Callable[[], None]], None]:
        return self.decorator(tokens)

    def decorator(
        self,
        tokens: tuple[str, ...],
    ) -> Callable:
        def _wrapper(
            func,
        ) -> None:
            self.add_handler(
                tokens=tokens,
                handler=func,
            )

        return _wrapper

    async def check(
        self,
        api: TelegramBotAPI,
        update: Update,
    ) -> list[Coroutine[Any, Any, None]]:
        handlers_tasks, matchers_tasks = await gather(
            self.check_handlers(
                api=api,
                update=update,
            ),
            self._check_nested_matchers(
                api=api,
                update=update,
            ),
        )
        return handlers_tasks + matchers_tasks


class CommandMatcher(
    MatcherBase,
):
    def __init__(
        self,
        prefix: str = "",
        *,
        case_sensitive: bool = False,
    ) -> None:
        super().__init__()
        prefix = prefix.strip()
        if case_sensitive:
            prefix = prefix.lower()
        self._prefix = prefix
        self._case_sensitive = case_sensitive

    def check_condition(
        self,
        token: str,
        update: Update,
    ) -> bool:
        if not update.message or not update.message.text:
            return False
        token = self._prefix + token
        for word in update.message.text.split(" "):
            if not word:
                continue
            if self._case_sensitive and token.lower() == word.lower():
                return True
            if token == word:
                return True
        return False


class RegexMatcher(
    MatcherBase,
):
    def check_condition(
        self,
        token: str,  # type: ignore
        update: Update,
    ) -> bool:
        if not update.message or not update.message.text:
            return False
        if findall(token, update.message.text):
            return True
        return False
