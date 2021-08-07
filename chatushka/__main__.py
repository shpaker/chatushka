from asyncio import run
from datetime import datetime, timedelta, timezone
from logging import DEBUG, INFO, WARNING, basicConfig, getLogger
from random import choice, randrange
from typing import List

from httpx import AsyncClient

from chatushka.matchers import CommandsMatcher, CronMatcher, EventTypes, RegexMatcher
from chatushka.settings import get_settings
from chatushka.transports.models import ChatPermissions, Message
from chatushka.transports.telegram_bot_api import TelegramBotApi
from chatushka.watch_dog_bot import Chatushka

# https://urlregex.com/
JOKES_URL = "https://jokesrv.rubedo.cloud/"
EIGHT_BALL_EN = (
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes — definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Signs point to yes",
    "Yes",
    "Reply hazy, try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don’t count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful",
)
EIGHT_BALL_RU = (
    "Бесспорно",
    "Предрешено",
    "Никаких сомнений",
    "Определённо да",
    "Можешь быть уверен в этом",
    "Мне кажется — «да»",
    "Вероятнее всего",
    "Хорошие перспективы",
    "Знаки говорят — «да»",
    "Да",
    "Пока не ясно, попробуй снова",
    "Спроси позже",
    "Лучше не рассказывать",
    "Сейчас нельзя предсказать",
    "Сконцентрируйся и спроси опять",
    "Даже не думай",
    "Мой ответ — «нет»",
    "По моим данным — «нет»",
    "Перспективы не очень хорошие",
    "Весьма сомнительно",
)
logger = getLogger()
settings = get_settings()

on_commands = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
    allow_raw=True,
)
on_sensitive_commands = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
    allow_raw=False,
)
on_cron = CronMatcher()
on_regex = RegexMatcher()


async def check_preconditions(
    api: TelegramBotApi,
) -> None:
    response = await api.get_me()
    logger.debug(response.json(indent=2))
    if not response.can_join_groups:
        raise RuntimeError("Talk to @botfather and enable groups access for bot.")
    if not response.can_read_all_group_messages:
        raise RuntimeError("Talk to @botfather and disable the privacy mode.")


@on_regex(r"\?")  # type: ignore
async def on_question_command(
    api: TelegramBotApi,
    message: Message,
    matched: List[str],  # noqa, pylint: disable=unused-argument
) -> None:
    rand_int = randrange(5)
    if rand_int == 3:
        await api.send_message(
            chat_id=message.chat.id,
            text=choice(EIGHT_BALL_RU),
            reply_to_message_id=message.message_id,
        )


# @on_cron("*/1 * * * *")
# def reminder_on_cron():
#     logger.debug(777777)


@on_commands("id")
async def on_id_command(
    api: TelegramBotApi,
    message: Message,
) -> None:
    logger.debug(f"id request from {message.user.readable_name} (id={message.user.id})")
    await api.send_message(
        chat_id=message.chat.id,
        text=f"Your telegram identifier is <pre>{message.user.id}</pre>",
        reply_to_message_id=message.message_id,
    )


@on_commands("8ball", "8ball", "шарик")  # type: ignore
async def on_8ball_command(
    api: TelegramBotApi,
    message: Message,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text=choice(EIGHT_BALL_RU),
        reply_to_message_id=message.message_id,
    )


@on_commands("joke", "анекдот", "шутка")  # type: ignore
async def on_joke_command(
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


@on_sensitive_commands("mute")
async def on_mute_command(
    api: TelegramBotApi,
    message: Message,
    args: list[str],
) -> None:
    if message.user.id not in settings.admins:
        return None
    if not args:
        await api.send_message(
            chat_id=message.chat.id,
            text=f"🧐 уточни времянной период на который необходимо замьютить пользователя",
            reply_to_message_id=message.message_id,
        )
        return None

    if not message.reply_to_message:
        await api.send_message(
            chat_id=message.chat.id,
            text=f"🧐 Комманда должна быть реплаем",
            reply_to_message_id=message.message_id,
        )
        return None

    try:
        restrict_time = timedelta(hours=int(args[0]))
    except ValueError:
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
        text=f"Лапки коротковаты чтоб убить {message.user.readable_name}",
        reply_to_message_id=message.message_id,
    )


@on_sensitive_commands("suicide", "wtf")  # type: ignore
async def on_suicide_command(
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


def make_bot() -> Chatushka:
    instance = Chatushka(token=settings.token, debug=settings.debug)
    instance.add_matcher(on_commands)
    instance.add_matcher(on_sensitive_commands)
    instance.add_matcher(on_cron)
    instance.add_matcher(on_regex)
    instance.add_handler(EventTypes.STARTUP, check_preconditions)
    return instance


def main():
    basicConfig(level=DEBUG if settings.debug else INFO)
    logger.debug("Debug mode is on".upper())
    getLogger("httpx").setLevel(WARNING)
    bot = make_bot()
    run(bot.serve())


if __name__ == "__main__":
    main()
