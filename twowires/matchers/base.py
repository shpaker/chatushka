from abc import ABC, abstractmethod
from asyncio import iscoroutinefunction
from collections import defaultdict
from typing import Iterable, Union, Callable, Any, Optional, Hashable

from twowires.transports.models import Message
from twowires.matchers.protocols import MatcherProtocol
from twowires.matchers.types import HANDLER_TYPING, MatchedToken


class MatcherBase(ABC, MatcherProtocol):

    handlers: dict[Hashable, list[HANDLER_TYPING]] = defaultdict(list)

    def decorator(
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
        for raw_token in tokens:
            prepared = self._cast_token(raw_token.strip())
            if not isinstance(prepared, (list, tuple, set)):
                prepared = (prepared,)
            for token in prepared:
                self.handlers[token].append(handler)

    async def match(
        self,
        message: Message,
    ) -> MatchedToken:
        for token in self.handlers.keys():
            if matched := await self._check(token, message):
                await self.call(
                    token=matched.token,
                    message=message,
                    args=matched.args,
                    kwargs=matched.kwargs,
                )
                return matched

    async def call(
        self,
        token: Hashable,
        message: Optional[Message] = None,
        args: tuple[str] = tuple(),
        kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        if not kwargs:
            kwargs = dict()
        kwargs | dict(message=message, token=token)
        handlers = self.handlers[token]
        for handler in handlers:
            if iscoroutinefunction(handler):
                await handler(*args, **kwargs)  # type: ignore
                return
            handler(*args, **kwargs)

    async def _cast_token(
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
