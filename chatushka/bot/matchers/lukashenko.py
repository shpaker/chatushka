from random import choice

from chatushka.bot.internal.data_dir import read_txt_from_data_dir
from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher
from chatushka.core.transports.models import Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

settings = get_settings()
lukashenko_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)


@lukashenko_matcher(
    "lukashenko",
    "luk",
    "lag",
    help_message="Quotes by Alexander G. Lukashenko",
)
async def lukashenko_handler(
    api: TelegramBotApi,
    message: Message,
) -> None:
    quotes = read_txt_from_data_dir("lukashenko.txt")
    await api.send_message(
        chat_id=message.chat.id,
        text=choice(quotes),
        reply_to_message_id=message.message_id,
    )
