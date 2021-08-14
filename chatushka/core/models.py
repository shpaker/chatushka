from enum import Enum, auto, unique
from typing import Any, Callable, Coroutine, Hashable, NamedTuple, TypedDict, Union

# pylint: disable=invalid-name
HANDLER_TYPING = Union[
    Callable[[Any], None],
    Callable[[Any], Coroutine[Any, Any, Any]],
]


class RegexMatchKwargs(TypedDict):
    matched: tuple[str, ...]


class MatchedToken(NamedTuple):
    token: Hashable
    args: tuple[str, ...] = ()
    kwargs: dict[str, Any] = dict()


@unique
class EventTypes(Enum):
    STARTUP = auto()
    SHUTDOWN = auto()
    MESSAGE = auto()
