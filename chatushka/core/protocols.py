from collections.abc import Callable, Coroutine, Hashable, Iterable
from typing import Any, Protocol

from chatushka.core.models import HANDLER_TYPING, MatchedToken, Message
from chatushka.core.telegram import Telegram


class MatcherProtocol(Protocol):
    handlers: dict[Hashable, list[HANDLER_TYPING]]

    def __call__(
        self,
        *tokens: Hashable,
    ) -> Callable[[Callable[[], None]], None]:
        ...

    def add_handler(
        self,
        tokens: Hashable | Iterable[Hashable],
        handler: Callable[[], None] | Callable[[], Coroutine],  # type: ignore
    ) -> None:
        ...

    async def check_handlers(
        self,
        message: Message,
    ) -> None:
        ...

    async def match(
        self,
        api: Telegram,
        message: Message,
    ) -> MatchedToken:
        ...

    async def call(
        self,
        api: Telegram,
        token: Hashable,
        message: Message | None = None,
        kwargs: dict[str, Any] | None = None,
    ) -> None:
        ...

    async def init(self) -> None:
        ...
