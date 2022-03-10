from abc import ABC
from asyncio import iscoroutinefunction
from collections import defaultdict
from inspect import signature
from typing import Any, Callable, Hashable, Iterable, NamedTuple, Optional, Union

from chatushka.core.models import HANDLER_TYPING, MatchedToken
from chatushka.core.protocols import MatcherProtocol
from chatushka.core.transports.models import Update
from chatushka.core.transports.telegram_bot_api import TelegramBotApi


class HelpMessage(NamedTuple):
    tokens: tuple[str]
    message: Optional[str]


class MatcherBase(ABC):
    def __init__(
        self,
    ) -> None:
        self.handlers: dict[Hashable, list[HANDLER_TYPING]] = defaultdict(list)
        self.matchers: list[MatcherProtocol] = []
        self._help_messages: list[HelpMessage] = []

    def __call__(
        self,
        *tokens: Hashable,
        help_message: Optional[str] = None,
        include_in_help: bool = True,
    ) -> Callable[[Callable[[], None]], None]:
        def decorator(
            func: HANDLER_TYPING,
        ) -> None:
            self.add_handler(
                tokens=tokens,
                handler=func,
                help_message=help_message,
                include_in_help=include_in_help,
            )

        return decorator

    @property
    def help_messages(self):
        messages = self._help_messages.copy()
        for matcher in self.matchers:
            messages += matcher.help_messages
        return messages

    def add_handler(
        self,
        tokens: Union[Hashable, Iterable[Hashable]],
        handler: HANDLER_TYPING,
        help_message: Optional[str] = None,
        include_in_help: bool = True,
    ) -> None:
        if not help_message:
            help_message = f"help message of {self.__class__.__name__}"
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
        if include_in_help:
            self._help_messages.append(
                HelpMessage(tokens, help_message),
            )

    def add_matcher(
        self,
        *matchers: MatcherProtocol,
    ) -> None:
        self.matchers += matchers

    async def match(
        self,
        api: TelegramBotApi,
        update: Update,
        *,
        should_call_matched: bool = False,
    ) -> list[MatchedToken]:
        matched_handlers = []
        for token in self.handlers.keys():
            if matched := await self._check(token, update):
                matched_handlers.append(matched)
                if should_call_matched:
                    await self.call(
                        api=api,
                        token=matched.token,
                        update=update,
                        kwargs=matched.kwargs | dict(args=matched.args),
                    )
        for matcher in self.matchers:
            matched_handlers += await matcher.match(api, update, should_call_matched=should_call_matched)
        return matched_handlers

    async def call(
        self,
        api: TelegramBotApi,
        token: Hashable,
        update: Optional[Update] = None,
        kwargs: Optional[dict[str, Any]] = None,
    ) -> None:
        if not kwargs:
            kwargs = {}
        kwargs = kwargs | dict(api=api, update=update, token=token)
        handlers = self.handlers.get(token)
        if not handlers:
            return
        for handler in handlers:
            sig = signature(handler)
            sig_kwargs = {param: kwargs.get(param) for param in sig.parameters if param in kwargs}
            if update and update.message is not None and "message" in sig.parameters:
                sig_kwargs["message"] = update.message
            if iscoroutinefunction(handler):
                await handler(**sig_kwargs)  # type: ignore
                continue
            handler(**sig_kwargs)

    # pylint: disable=no-self-use
    def _cast_token(
        self,
        token: Hashable,
    ) -> Union[Any, Iterable[Any]]:
        return (token,)  # noqa

    # pylint: disable=unused-argument
    async def _check(
        self,
        token: Hashable,
        update: Update,
    ) -> Optional[MatchedToken]:
        return None

    async def init(self) -> None:
        pass
