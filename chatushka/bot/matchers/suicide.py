from datetime import datetime, timedelta, timezone
from random import randrange

from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher
from chatushka.core.transports.models import ChatPermissions, Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

settings = get_settings()
suicide_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)


@suicide_matcher("suicide", "wtf")
async def suicide_handler(
    api: TelegramBotApi,
    message: Message,
) -> None:
    restrict_time = timedelta(minutes=randrange(1, 4 * 60))
    try:
        is_success = await api.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
            ),
            until_date=datetime.now(tz=timezone.utc) + restrict_time,
        )
    except ValueError:
        is_success = False
    if is_success:
        await api.send_message(
            chat_id=message.chat.id,
            text=f"Пользователь {message.user.readable_name} самовыпилился на {restrict_time}",
        )
        return None
    await api.send_message(
        chat_id=message.chat.id,
        text=f"Лапки коротковаты чтоб убить {message.user.readable_name}",
        reply_to_message_id=message.message_id,
    )
