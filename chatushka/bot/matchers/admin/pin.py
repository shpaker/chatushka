from asyncio import sleep

from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher
from chatushka.core.transports.models import Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

settings = get_settings()
pin_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)


@pin_matcher("pin")
async def pin_handler(
    api: TelegramBotApi,
    message: Message,
    args: list[str],
) -> None:
    if not message.reply_to_message:
        await api.send_message(
            chat_id=message.chat.id,
            text="Для закрепа необходимо написать команду реплаем",
            reply_to_message_id=message.message_id,
        )

    try:
        pin_hours = int(args[0])
    except (ValueError, IndexError):
        pin_hours = None

    _ = await api.pin_chat_message(
        chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id,
    )
    if pin_hours:
        await api.send_message(
            chat_id=message.chat.id,
            text=f"Через {pin_hours} ч. закреп будет убран",
            reply_to_message_id=message.message_id,
        )
        await sleep(pin_hours * 60)
        await api.unpin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id,
        )


@pin_matcher("unpin")
async def unpin_handler(
    api: TelegramBotApi,
    message: Message,
) -> None:
    await api.unpin_chat_message(
        chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id,
    )
