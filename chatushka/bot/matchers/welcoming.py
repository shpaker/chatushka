from random import randrange

from chatushka.bot.settings import get_settings
from chatushka.core.matchers import ChatUsersMovementsEventsEnum, ChatUsersMovementsMatcher, CommandsMatcher
from chatushka.core.transports.models import Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

settings = get_settings()
welcoming_matcher = ChatUsersMovementsMatcher()
_captcha_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)
welcoming_matcher.add_matcher(_captcha_matcher)

blocked_users: dict[int, int] = {}

_MAX_INT_IN_CAPTCHA = 51
_BLOCK_TIMEOUT_MINUTES = 10


@welcoming_matcher(ChatUsersMovementsEventsEnum.CAME, include_in_help=False)
async def came_handler(
    api: TelegramBotApi,
    message: Message,
) -> None:
    for user in message.new_chat_members:
        first_int = randrange(1, _MAX_INT_IN_CAPTCHA)
        second_int = randrange(1, _MAX_INT_IN_CAPTCHA)
        text = (
            f'Привет, <a href="tg://user?id={user.id}">{user.readable_name}</a>!\n'
            f"Все твои сообщения будут удаляться, а сам ты будешь удален из чата через {_BLOCK_TIMEOUT_MINUTES} "
            f"минут если не напишешь боту ответ на задачку:\n<b>{first_int}+{second_int}=?</b>.\n"
            f"Сообщение для бота необходимо начать с комманды <pre>!captcha</pre>.\n"
            f"Пример: <pre>!captcha {randrange(1, _MAX_INT_IN_CAPTCHA*2-2)}</pre>"
        )
        blocked_users[user.id] = first_int + second_int
        await api.send_message(
            chat_id=message.chat.id,
            text=text,
        )


@_captcha_matcher("captcha")
async def captcha_handler(
    api: TelegramBotApi,
    message: Message,
    args: list[str],
) -> None:
    if message.user.id not in blocked_users or len(args) < 1:
        return
    try:
        captcha_code = int(args[0])
    except ValueError:
        return
    if captcha_code == blocked_users[message.user.id]:
        del blocked_users[message.user.id]
        await api.send_message(
            chat_id=message.chat.id,
            text="YES!",
            reply_to_message_id=message.message_id,
        )
        return
    await api.send_message(
        chat_id=message.chat.id,
        text="NO!",
        reply_to_message_id=message.message_id,
    )
