from httpx import AsyncClient

from chatushka.bot.settings import BOBUK_JOKES_URL, get_settings
from chatushka.core.matchers import CommandsMatcher
from chatushka.core.transports.models import Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

settings = get_settings()
jokes_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)


@jokes_matcher("jokes", "joke")
async def jokes_handler(
    api: TelegramBotApi,
    message: Message,
) -> None:
    async with AsyncClient() as client:  # type: AsyncClient
        response = await client.get(BOBUK_JOKES_URL)
        try:
            response.raise_for_status()
            joke = response.json()["content"]
        except Exception:  # noqa, pylint: disable=broad-except
            return
    await api.send_message(
        chat_id=message.chat.id,
        text=joke,
    )
