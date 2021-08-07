from typing import Any, Callable, Coroutine, Hashable, Iterable, Optional, Protocol, Union

from chatushka.transports.models import Message
from chatushka.transports.telegram_bot_api import TelegramBotApi
from chatushka.types import HANDLER_TYPING, MatchedToken


class MatcherProtocol(Protocol):

    handlers: dict[Hashable, list[HANDLER_TYPING]]

    def __call__(
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
        api: TelegramBotApi,
        message: Message,
    ) -> MatchedToken:
        ...

    async def call(
        self,
        api: TelegramBotApi,
        token: Hashable,
        message: Optional[Message] = None,
        kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        ...

    async def init(self) -> None:
        ...
