from abc import ABC, abstractmethod
from asyncio import iscoroutinefunction
from collections import defaultdict
from inspect import signature
from typing import Any, Callable, Hashable, Iterable, Optional, Union

from twowires.matchers.protocols import MatcherProtocol
from twowires.matchers.types import HANDLER_TYPING, MatchedToken
from twowires.transports.models import Message
from twowires.transports.telegram_bot_api import TelegramBotApi


class MatcherBase(ABC, MatcherProtocol):

    handlers: dict[Hashable, list[HANDLER_TYPING]]

    def __init__(self):
        self.handlers = defaultdict(list)

    def __call__(
        self,
        *tokens: Hashable,
    ) -> Callable[[Callable[[], None]], None]:
        def decorator(
            func: HANDLER_TYPING,
        ) -> None:
            self.add_handler(tokens=tokens, handler=func)

        return decorator

    def add_handler(
        self,
        tokens: Union[Hashable, Iterable[Hashable]],
        handler: HANDLER_TYPING,
    ) -> None:
        if not isinstance(tokens, (list, tuple, set)):
            tokens = (tokens,)
        for raw_token in tokens:
            if isinstance(raw_token, str):
                raw_token = raw_token.strip()
            prepared = self._cast_token(raw_token)
            if not isinstance(prepared, (list, tuple, set)):
                prepared = (prepared,)
            for token in prepared:
                self.handlers[token].append(handler)

    async def match(
        self,
        api: TelegramBotApi,
        message: Message,
    ) -> MatchedToken:
        for token in self.handlers.keys():
            if matched := await self._check(token, message):
                await self.call(
                    api=api,
                    token=matched.token,
                    message=message,
                    args=matched.args,
                    kwargs=matched.kwargs,
                )
                return matched

    async def call(
        self,
        api: TelegramBotApi,
        token: Hashable,
        message: Optional[Message] = None,
        args: tuple[str] = tuple(),
        kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        if not kwargs:
            kwargs = dict()
        kwargs = kwargs | dict(api=api, message=message, token=token)
        handlers = self.handlers.get(token)
        if not handlers:
            return
        for handler in handlers:
            sig = signature(handler)
            sig_kwargs = {param: kwargs.get(param) for param in sig.parameters if param in kwargs}
            if iscoroutinefunction(handler):
                await handler(**sig_kwargs)  # type: ignore
                return
            handler(**sig_kwargs)

    def _cast_token(
        self,
        token: Hashable,
    ) -> Union[Any, Iterable[Any]]:
        return (token,)

    @abstractmethod
    async def _check(
        self,
        token: Hashable,
        message: Message,
    ) -> Optional[MatchedToken]:
        raise NotImplementedError
