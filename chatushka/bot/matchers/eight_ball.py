from random import choice, randrange

from chatushka.bot.internal.data_dir import read_yaml_from_data_dir
from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher, RegexMatcher
from chatushka.core.transports.models import Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

HELP_MESSAGE = (
    'Just think of a question that can be answered "Yes" or "No", concentrate very, very hard, and type command!'
)

settings = get_settings()
eight_ball_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)
question_matcher = RegexMatcher()
eight_ball_matcher.add_matcher(question_matcher)


@eight_ball_matcher("8ball", "ball8", "b8", "8b", help_message=HELP_MESSAGE)
async def eight_ball_handler(
    api: TelegramBotApi,
    message: Message,
) -> None:
    answers = read_yaml_from_data_dir("eight_ball")
    await api.send_message(
        chat_id=message.chat.id,
        text=choice(answers["ru"]),
        reply_to_message_id=message.message_id,
    )


@question_matcher(r"\?", include_in_help=False)
async def eight_ball_answer_handler(
    api: TelegramBotApi,
    message: Message,
    matched: list[str],  # noqa, pylint: disable=unused-argument
) -> None:
    answers = read_yaml_from_data_dir("eight_ball")
    rand_int = randrange(8)
    if rand_int == 1:
        await api.send_message(
            chat_id=message.chat.id,
            text=choice(answers["ru"]),
            reply_to_message_id=message.message_id,
        )
