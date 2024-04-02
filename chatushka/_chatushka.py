from collections.abc import Callable
from re import RegexFlag
from typing import Any, final

from chatushka._bot import MatchersBot
from chatushka._matchers import CommandMatcher, EventMatcher, RegExMatcher
from chatushka._models import Events


@final
class Chatushka(
    MatchersBot,
):
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
            self.add(
                CommandMatcher(
                    *commands,
                    action=func,
                    case_sensitive=case_sensitive,
                    chance_rate=chance_rate,
                    results_model=results_model,
                )
            )

        return _wrapper

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
            self.add(
                RegExMatcher(
                    *patterns,
                    action=func,
                    re_flags=re_flags,
                    chance_rate=chance_rate,
                    results_model=results_model,
                )
            )

        return _wrapper

    def event(
        self,
        *events: Events,
        chance_rate: float = 1.0,
        results_model: type[Any] | None = None,
    ) -> Callable:
        def _wrapper(
            func,
        ) -> None:
            self.add(
                EventMatcher(
                    *events,
                    action=func,
                    chance_rate=chance_rate,
                    results_model=results_model,
                )
            )

        return _wrapper
