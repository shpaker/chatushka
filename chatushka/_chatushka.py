from asyncio import gather
from collections.abc import AsyncGenerator, Callable, MutableMapping, Sequence
from contextlib import (
    AbstractAsyncContextManager,
    asynccontextmanager,
)
from re import RegexFlag
from typing import Any, final

from chatushka.__version__ import __version__
from chatushka._constants import (
    HTTP_POOLING_TIMEOUT,
)
from chatushka._errors import ChatushkaResponseError
from chatushka._logger import logger
from chatushka._matchers import CommandMatcher, EventMatcher, Matcher, RegExMatcher
from chatushka._models import Events
from chatushka._sentry import report_exc
from chatushka._transport import TelegramBotAPI


@asynccontextmanager
async def _default_lifespan(
    _: "Chatushka",
) -> AsyncGenerator[None, None]:
    yield


@final
class Chatushka:
    def __init__(
        self,
        *,
        token: str,
        cmd_prefixes: str | Sequence[str] = (),
        lifespan: AbstractAsyncContextManager | None = None,
    ) -> None:
        self._state: MutableMapping = {}
        self._lifespan = lifespan or _default_lifespan
        self._token = token
        if isinstance(cmd_prefixes, str):
            cmd_prefixes = [cmd_prefixes]
        self._cmd_prefixes = cmd_prefixes
        self._matchers: list[Matcher] = []  # type: ignore

    def __repr__(
        self,
    ) -> str:
        return f"<{self.__class__.__name__} {__version__}: {len(self._matchers)} matchers>"

    def add_matcher(
        self,
        matcher: Matcher,
    ) -> None:
        if isinstance(matcher, CommandMatcher):
            matcher.add_commands_prefixes(
                self._cmd_prefixes,
            )
        logger.info(f"{self} + {matcher}")
        self._matchers.append(matcher)

    def add_cmd(
        self,
        *commands: str,
        action: Callable,
        case_sensitive: bool = False,
        chance_rate: float = 1.0,
        results_model: type[Any] | None = None,
    ) -> None:
        self.add_matcher(
            CommandMatcher(
                *commands,
                action=action,
                case_sensitive=case_sensitive,
                chance_rate=chance_rate,
                results_model=results_model,
            )
        )

    def cmd(
        self,
        *commands: str,
        case_sensitive: bool = False,
        chance_rate: float = 1.0,
        results_model: type[Any] | None = None,
    ) -> Callable:
        def _wrapper(
            func,
        ) -> None:
            self.add_cmd(
                *commands,
                action=func,
                case_sensitive=case_sensitive,
                chance_rate=chance_rate,
                results_model=results_model,
            )

        return _wrapper

    def add_regex(
        self,
        *patterns: str,
        action: Callable,
        re_flags: int | RegexFlag = 0,
        chance_rate: float = 1.0,
        results_model: type[Any] | None = None,
    ) -> None:
        self.add_matcher(
            RegExMatcher(
                *patterns,
                action=action,
                re_flags=re_flags,
                chance_rate=chance_rate,
                results_model=results_model,
            )
        )

    def regex(
        self,
        *patterns: str,
        re_flags: int | RegexFlag = 0,
        chance_rate: float = 1.0,
        results_model: type[Any] | None = None,
    ) -> Callable:
        def _wrapper(
            func,
        ) -> None:
            self.add_regex(
                *patterns,
                action=func,
                re_flags=re_flags,
                chance_rate=chance_rate,
                results_model=results_model,
            )

        return _wrapper

    def add_event(
        self,
        *events: Events,
        action: Callable,
        chance_rate: float = 1.0,
        results_model: type[Any] | None = None,
    ) -> None:
        self.add_matcher(
            EventMatcher(
                *events,
                action=action,
                chance_rate=chance_rate,
                results_model=results_model,
            )
        )

    def event(
        self,
        *events: Events,
        chance_rate: float = 1.0,
        results_model: type[Any] | None = None,
    ) -> Callable:
        def _wrapper(
            func,
        ) -> None:
            self.add_event(
                *events,
                action=func,
                chance_rate=chance_rate,
                results_model=results_model,
            )

        return _wrapper

    async def _check_updates(
        self,
        api: TelegramBotAPI,
        offset: int | None,
    ) -> int | None:
        try:
            updates, offset = await api.get_updates(offset)
        except (Exception, ChatushkaResponseError) as exc:
            report_exc(exc)
            return offset
        if not updates:
            return offset
        logger.debug(f"{self} <<< {len(updates)} updates from {offset=}")
        results = await gather(
            *[
                matcher(  # type: ignore
                    api=api,
                    update=update,
                )
                for update in updates
                for matcher in self._matchers
            ],
            return_exceptions=True,
        )
        for result in results:
            if isinstance(result, Exception):
                report_exc(result)
        return offset

    async def _loop(
        self,
    ) -> None:
        offset: int | None = None
        while True:
            async with TelegramBotAPI(
                token=self._token,
                timeout=HTTP_POOLING_TIMEOUT,
            ) as api:
                offset = await self._check_updates(
                    api=api,
                    offset=offset,
                )

    async def run(
        self,
    ) -> None:
        logger.info(f"{self} (っ◔◡◔)っ start polling")
        async with self._lifespan(  # type: ignore
            self,
        ):
            await self._loop()
