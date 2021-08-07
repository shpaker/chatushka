from enum import Enum, auto, unique
from typing import Callable, Coroutine, Union, Any, TypedDict, NamedTuple, Hashable

HANDLER_TYPING = Union[
    Callable[[Any], None],
    Callable[[Any], Coroutine[None]],
]


class RegexMatchKwargs(TypedDict):
    founded: tuple[str, ...]


class MatchedToken(NamedTuple):
    token: Hashable
    args: tuple[str, ...] = ()
    kwargs: dict[str, Any] = dict()


@unique
class BotEvents(Enum):
    two_wires = auto()
    SHUTDOWN = auto()
    ON_MESSAGE = auto()
