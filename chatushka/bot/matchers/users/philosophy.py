from random import randrange

from chatushka import CommandsMatcher, Message, RegexMatcher, Telegram
from chatushka.bot.settings import get_settings

_RESPONSE = "Зависит от контекста"

settings = get_settings()
is_four_a_lot_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)
philosophy_matcher = RegexMatcher()


@philosophy_matcher(r"([/!]$)")
async def exclamation_handler(
    api: Telegram,
    message: Message,
    matched: list[str],  # pylint: disable=unused-argument
) -> None:
    rand_int = randrange(16)
    if rand_int == 1:
        await api.send_message(
            chat_id=message.chat.id,
            text=_RESPONSE,
            reply_to_message_id=message.message_id,
        )


@philosophy_matcher(r"((\s|^)(([\d]*|[а-яА-Я]*) это много/?)|((\s|^)Is ([\d]*|[a-zA-Z]*) a lot/?))")
async def philosophy_handler(
    api: Telegram,
    message: Message,
    matched: list[str],  # pylint: disable=unused-argument
) -> None:
    rand_int = randrange(4)
    if rand_int == 1:
        await api.send_message(
            chat_id=message.chat.id,
            text=_RESPONSE,
            reply_to_message_id=message.message_id,
        )
