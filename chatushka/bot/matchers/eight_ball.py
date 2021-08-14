from random import choice, randrange

from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher, RegexMatcher
from chatushka.core.transports.models import Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

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

settings = get_settings()
eight_ball_command_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)
eight_ball_question_matcher = RegexMatcher()
eight_ball_matchers = (
    eight_ball_command_matcher,
    eight_ball_question_matcher,
)


@eight_ball_command_matcher("8ball", "ball8", "b8", "8b")
async def eight_ball_handler(
    api: TelegramBotApi,
    message: Message,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text=choice(EIGHT_BALL_RU),
        reply_to_message_id=message.message_id,
    )


@eight_ball_question_matcher(r"\?")
async def eight_ball_answer_handler(
    api: TelegramBotApi,
    message: Message,
    matched: list[str],  # noqa, pylint: disable=unused-argument
) -> None:
    rand_int = randrange(5)
    if rand_int == 3:
        await api.send_message(
            chat_id=message.chat.id,
            text=choice(EIGHT_BALL_RU),
            reply_to_message_id=message.message_id,
        )
