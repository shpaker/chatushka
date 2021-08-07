from chatushka.transports.models import Message
from chatushka.transports.telegram_bot_api import TelegramBotApi


async def user_id(
    api: TelegramBotApi,
    message: Message,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text=f"Your telegram identifier is <pre>{message.user.id}</pre>",
        reply_to_message_id=message.message_id,
    )
