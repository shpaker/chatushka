from httpx import AsyncClient

from chatushka.transports.models import Message
from chatushka.transports.telegram_bot_api import TelegramBotApi

JOKES_URL = "https://jokesrv.rubedo.cloud/"


async def joke(
    api: TelegramBotApi,
    message: Message,
) -> None:
    async with AsyncClient() as client:  # type: AsyncClient
        response = await client.get(JOKES_URL)
        try:
            response.raise_for_status()
            joke = response.json()["content"]

        except Exception:  # noqa, pylint: disable=broad-except
            return
    await api.send_message(
        chat_id=message.chat.id,
        text=joke,
    )
