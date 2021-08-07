from datetime import datetime, timedelta, timezone
from random import randrange

from chatushka.transports.models import ChatPermissions, Message
from chatushka.transports.telegram_bot_api import TelegramBotApi


async def suicide(
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


async def mute(
    api: TelegramBotApi,
    message: Message,
    args: list[str],
) -> None:

    if not message.reply_to_message:
        await api.send_message(
            chat_id=message.chat.id,
            text=f"🧐 Комманда должна быть реплаем",
            reply_to_message_id=message.message_id,
        )
        return None

    try:
        restrict_time = timedelta(hours=int(args[0]))
    except (ValueError, IndexError):
        restrict_time = timedelta(minutes=randrange(10, 30))
        await api.send_message(
            chat_id=message.chat.id,
            text=f"🧐 не удалось спарсить значение и я решил, "
                 f"что надо замьютить {message.reply_to_message.user.readable_name} "
                 f"на {restrict_time} минут",
            reply_to_message_id=message.message_id,
        )

    try:
        is_success = await api.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.user.id,
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
            text=f"Пользователь {message.reply_to_message.user.readable_name} принял обет молчания",
        )
        return None
    await api.send_message(
        chat_id=message.chat.id,
        text=f"Лапки коротковаты чтоб покарать {message.reply_to_message.user.readable_name}",
        reply_to_message_id=message.message_id,
    )
