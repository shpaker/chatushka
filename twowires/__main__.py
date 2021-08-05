from asyncio import run
from datetime import datetime, timedelta, timezone
from logging import DEBUG, INFO, basicConfig, getLogger
from random import choice, randrange
from typing import List

from httpx import AsyncClient
from meta_parser import __version__ as version_info

from twowires.models import ChatPermissions, Message
from twowires.settings import get_settings
from twowires.watch_dog_bot import WatchDogBot

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
bot = WatchDogBot(settings.token)


@bot.on_event("startup")
def config_logger() -> None:
    log_level = DEBUG if settings.debug else INFO
    basicConfig(level=log_level)


@bot.on_event("startup")  # type: ignore
async def check_preconditions() -> None:
    response = await bot.api.get_me()
    logger.info(response.json(indent=2))
    if not response.can_join_groups:
        raise RuntimeError("Talk to @botfather and enable groups access for bot.")
    if not response.can_read_all_group_messages:
        raise RuntimeError("Talk to @botfather and disable the privacy mode.")


@bot.on_command("version")  # type: ignore
async def on_version_command(
    message: Message,
) -> None:
    await bot.api.send_message(
        chat_id=message.chat.id,
        text=f'<a href="{version_info.__url__}">{version_info.__title__} {version_info.__version__}</a>',
        reply_to_message_id=message.message_id,
    )


@bot.on_command("id")  # type: ignore
async def on_id_command(
    message: Message,
) -> None:
    await bot.api.send_message(
        chat_id=message.chat.id,
        text=f"Your telegram identifier is <pre>{message.user.id}</pre>",
        reply_to_message_id=message.message_id,
    )


@bot.on_command("8ball")  # type: ignore
async def on_8ball_command(
    message: Message,
) -> None:
    await bot.api.send_message(
        chat_id=message.chat.id,
        text=choice(EIGHT_BALL_RU),
        reply_to_message_id=message.message_id,
    )


@bot.on_message(r"\?")  # type: ignore
async def on_question_command(
    message: Message,
    matched: List[str],  # noqa, pylint: disable=unused-argument
) -> None:
    rand_int = randrange(5)
    if rand_int == 3:
        await bot.api.send_message(
            chat_id=message.chat.id,
            text=choice(EIGHT_BALL_RU),
            reply_to_message_id=message.message_id,
        )


@bot.on_command("joke")  # type: ignore
async def on_joke_command(
    message: Message,
) -> None:
    async with AsyncClient() as client:  # type: AsyncClient
        response = await client.get(JOKES_URL)
        try:
            response.raise_for_status()
            joke = response.json()["content"]

        except Exception:  # noqa, pylint: disable=broad-except
            return
    await bot.api.send_message(
        chat_id=message.chat.id,
        text=joke,
    )


@bot.on_command("suicide")  # type: ignore
async def on_suicide_command(
    message: Message,
) -> None:
    restrict_time = timedelta(minutes=randrange(1, 12 * 60))
    try:
        is_success = await bot.api.restrict_chat_member(
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
    except Exception as err:  # noqa, pylint: disable=broad-except
        logger.warning(err)
        await bot.api.send_message(
            chat_id=message.chat.id,
            text=f"Лапки коротковаты чтоб убить {message.user.readable_name}",
            reply_to_message_id=message.message_id,
        )
        return
    if is_success:
        await bot.api.send_message(
            chat_id=message.chat.id,
            text=f"Пользователь {message.user.readable_name} самовыпилился на {str(restrict_time)}",
        )


if __name__ == "__main__":
    run(bot.serve())
