from asyncio import gather

from chatushka._constants import (
    HTTP_POOLING_TIMEOUT,
)
from chatushka._handlers import id_handler, ping_handler
from chatushka._matchers import CommandMatcher, MatchersContainer
from chatushka._transport import TelegramBotAPI


class ChatushkaBot(
    MatchersContainer,
):
    def __init__(
        self,
        token: str,
    ) -> None:
        super().__init__()
        self._token = token
        self.setup_default_handlers()

    def setup_default_handlers(
        self,
    ) -> None:
        matcher = CommandMatcher(
            prefixes=["!", "/"],
        )
        matcher.add_handler("id", id_handler)
        matcher.add_handler("ping", ping_handler)
        self.add_matcher(matcher)

    async def _check_updates(
        self,
    ) -> None:
        async with TelegramBotAPI(
            token=self._token,
            timeout=HTTP_POOLING_TIMEOUT,
        ) as api:
            if not (updates := await api.get_updates()):
                return
            matched = []
            for update in updates:
                matched += await self._check_nested_matchers(
                    api=api,
                    update=update,
                )
            if matched:
                await gather(*matched)

    async def start(
        self,
    ) -> None:
        while True:
            await self._check_updates()
