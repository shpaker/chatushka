from datetime import datetime, timedelta, timezone
from enum import Enum
from random import choice, randrange
from typing import Optional

from chatushka.transports.models import ChatPermissions, Message, User
from chatushka.transports.telegram_bot_api import TelegramBotApi

RESTRICT_PERMISSION = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
)


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


class MuteMessages(Enum):
    ACCIDENT = (
        '🧐 <a href="tg://user?id={user}">{name}</a> споткнулся и упал. Попал в больницу на {time} минут.',
        '🧐 <a href="tg://user?id={user}">{name}</a> заигрался револьвером и угодил в травмпункт на {time} минут.',
        '🧐 <a href="tg://user?id={user}">{name}</a> переводил бабушку через дорогу и теперь отдыхает {time} минут.',
    )
    LOOSER = (
        '🧐 <a href="tg://user?id={looser_id}">{looser_name}</a> хотел убить '
        '<a href="tg://user?id={victim_id}">{victim_name}</a>, но что-то пошло не так и он '
        "вынужден провести в тюрьме {time} минут",
    )


async def mute_handler(
    api: TelegramBotApi,
    message: Message,
    args: list[str],
) -> None:
    admins = await api.get_chat_administrators(message.chat.id)
    privileges = None
    for admin in admins:
        if admin.user.id == message.user.id:
            privileges = admin
            break

    restrict_text = None
    restrict_user: Optional[User] = None
    restrict_time = None

    if not privileges or not (privileges.can_restrict_members or privileges.status.CREATOR):
        restrict_user = message.user
        restrict_time = timedelta(minutes=randrange(10, 30))
        text_tmpl = choice(MuteMessages.ACCIDENT.value)
        restrict_text = text_tmpl.format(
            user=restrict_user.id,
            name=restrict_user.readable_name,
            time=restrict_time.total_seconds() // 60,
        )

    if not message.reply_to_message:
        restrict_user = message.user
        restrict_time = timedelta(minutes=randrange(10, 30))
        text_tmpl = choice(MuteMessages.LOOSER.value)
        restrict_text = text_tmpl.format(
            looser_id=restrict_user.id,
            looser_name=restrict_user.readable_name,
            victim_id=message.reply_to_message.user.id,
            victim_name=message.reply_to_message.user.readable_name,
            time=restrict_time.total_seconds() // 60,
        )

    if not restrict_user:
        restrict_user = message.reply_to_message.user

    try:
        if not restrict_time:
            restrict_time = timedelta(hours=int(args[0]))
    except (ValueError, IndexError):
        restrict_time = timedelta(minutes=randrange(10, 30))
        text = (
            f'🧐 <a href="tg://user?id={restrict_user.id}">{restrict_user.readable_name}</a> будет молчать ровно'
            f" {restrict_time.total_seconds() // 60} минут"
        )
        await api.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_to_message_id=message.message_id,
        )

    try:
        is_success = await api.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=restrict_user.id,
            permissions=RESTRICT_PERMISSION,
            until_date=datetime.now(tz=timezone.utc) + restrict_time,
        )
    except ValueError:
        is_success = False

    if not restrict_text:
        restrict_text = (
            f'Пользователь <a href="tg://user?id={restrict_user.id}">{restrict_user.readable_name}</a> '
            f"принял обет молчания"
        )

    if is_success:
        await api.send_message(
            chat_id=message.chat.id,
            text=restrict_text,
        )
        return None
    await api.send_message(
        chat_id=message.chat.id,
        text=f"Лапки коротковаты чтоб покарать "
        f'<a href="tg://user?id={restrict_user.id}">{restrict_user.readable_name}</a>',
        reply_to_message_id=message.message_id,
    )
