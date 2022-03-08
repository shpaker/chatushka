from datetime import datetime, timedelta, timezone
from enum import Enum
from random import choice

from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher
from chatushka.core.transports.models import ChatPermissions, Message, User
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

RESTRICT_PERMISSION = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
)
settings = get_settings()
mute_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)


class MuteMessages(Enum):
    ACCIDENT = (
        '🧐 <a href="tg://user?id={user}">{name}</a> споткнулся, упал и попал в больницу на {time} минут.',
        '🧐 <a href="tg://user?id={user}">{name}</a> заигрался револьвером и угодил в травмпункт на {time} минут.',
        '🧐 <a href="tg://user?id={user}">{name}</a> переводил бабушку через дорогу и теперь отдыхает {time} минут.',
        '🧐 <a href="tg://user?id={user}">{name}</a> решил подумать о жизни {time} минут.',
    )
    LOOSER = (
        '🧐 <a href="tg://user?id={looser_id}">{looser_name}</a> хотел убить '
        '<a href="tg://user?id={victim_id}">{victim_name}</a>, но что-то пошло не так и он '
        "вынужден провести в тюрьме {time} минут",
        '🧐 У <a href="tg://user?id={looser_id}">{looser_name}</a> лапки коротковаты '
        'чтоб убить <a href="tg://user?id={victim_id}">{victim_name}</a>',
    )


async def send_mute_request(
    api: TelegramBotApi,
    message: Message,
    initiator: User,
    restrict_user: User,
    restrict_time: timedelta,
) -> None:
    text_tmpl = choice(MuteMessages.ACCIDENT.value)
    is_success = await api.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=restrict_user.id,
        permissions=RESTRICT_PERMISSION,
        until_date=datetime.now(tz=timezone.utc) + restrict_time,
    )
    if is_success:
        await api.send_message(
            chat_id=message.chat.id,
            text=text_tmpl.format(
                user=restrict_user.id,
                name=restrict_user.readable_name,
                time=int(restrict_time.total_seconds() // 60),
            ),
        )
        return
    text_tmpl = choice(MuteMessages.LOOSER.value)
    await api.send_message(
        chat_id=message.chat.id,
        text=text_tmpl.format(
            looser_id=initiator.id,
            looser_name=initiator.readable_name,
            victim_id=restrict_user.id,
            victim_name=restrict_user.readable_name,
        ),
        reply_to_message_id=message.message_id,
    )
