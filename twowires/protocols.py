from typing import Callable, Coroutine, Iterable, Protocol, Union

from twowires.models import Message


class Manager(Protocol):
    def decorator(
        self,
        *tokens: str,
    ) -> Callable[[Callable[[], None]], None]:
        ...

    def add_handler(
        self,
        tokens: Union[str, Iterable[str]],
        handler: Union[Callable[[], None], Callable[[], Coroutine]],  # type: ignore
    ) -> None:
        ...

    async def check_handlers(
        self,
        message: Message,
    ) -> None:
        ...
