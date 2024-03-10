from asyncio import gather

from chatushka._constants import (
    HTTP_POOLING_TIMEOUT,
    HTTP_REGULAR_TIMEOUT,
)
from chatushka._matchers import MatchersContainer
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

    async def serve(
        self,
    ) -> None:
        while True:
            async with TelegramBotAPI(
                token=self._token,
                timeout=HTTP_POOLING_TIMEOUT,
            ) as api:
                if not (updates := await api.get_updates()):
                    continue
            matched = []

            async with TelegramBotAPI(
                token=self._token,
                timeout=HTTP_REGULAR_TIMEOUT,
            ) as api:
                for update in updates:
                    matched += await self._check_nested_matchers(
                        api=api,
                        update=update,
                    )
                if matched:
                    await gather(*matched)
