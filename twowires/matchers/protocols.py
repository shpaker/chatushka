from typing import Callable, Coroutine, Iterable, Protocol, Union, Hashable, Any, Optional

from twowires.transports.models import Message
from twowires.matchers.types import HANDLER_TYPING, MatchedToken


class MatcherProtocol(Protocol):

    suffix: str
    handlers: dict[Hashable, list[HANDLER_TYPING]]

    def decorator(
        self,
        *tokens: Hashable,
    ) -> Callable[[Callable[[], None]], None]:
        ...

    def add_handler(
        self,
        tokens: Union[Hashable, Iterable[Hashable]],
        handler: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
    ) -> None:
        ...

    async def check_handlers(
        self,
        message: Message,
    ) -> None:
        ...

    async def match(
        self,
        message: Message,
    ) -> MatchedToken:
        ...

    async def call(
        self,
        token: Hashable,
        message: Optional[Message] = None,
        args: tuple[str] = tuple(),
        kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        ...
