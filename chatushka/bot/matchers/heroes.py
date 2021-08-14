from chatushka.bot.libs.heroes.cruds.activations import read_all_heroes_activations, set_heroes_activation
from chatushka.bot.libs.heroes.cruds.months import get_current_month
from chatushka.bot.libs.heroes.cruds.weeks import get_current_week
from chatushka.bot.libs.heroes.messages import extract_state
from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher, RegexMatcher
from chatushka.core.transports.models import Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

MESSAGE_TITLE = "✨💫 <b>ГЕРОЙСКИЙ КАЛЕНДАРЬ</b> 💫✨"
settings = get_settings()
heroes_commands_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)
heroes_regex_matcher = RegexMatcher()
heroes_matchers = (
    heroes_commands_matcher,
    heroes_regex_matcher,
)


@heroes_commands_matcher("homm", "heroes")
async def activate_heroes_handler(
    api: TelegramBotApi,
    message: Message,
    args: list[str],
) -> None:
    state = extract_state(args)
    if state is None:
        month = await get_current_month()
        week = await get_current_week()
        await api.send_message(
            chat_id=message.chat.id,
            text=(
                f"{MESSAGE_TITLE}\n"
                f"\n"
                f"<i>Выпуск №{month.number}/{week.number}\n</i>"
                f"\n"
                f"{month.message}\n"
                f"\n"
                f"{week.message}"
            ),
        )
        if not state:
            return
    await set_heroes_activation(
        user=message.user,
        chat=message.chat,
        state=state,
    )
    state_msg = (
        ('🙂 Подписка на периодическое издание "Геройский календарь" оформлена')
        if state
        else ('😏 Вы отписались от периодического издания "Геройский календарь"')
    )
    await api.send_message(
        chat_id=message.chat.id,
        text=state_msg,
        reply_to_message_id=message.message_id,
    )


@heroes_regex_matcher("2 4 1 * *")
async def heroes_month_handler(
    api: TelegramBotApi,
) -> None:
    activations = await read_all_heroes_activations()
    month = await get_current_month()
    for activation in activations:
        try:
            await api.send_message(
                chat_id=activation.chat_id,
                text=(f"{MESSAGE_TITLE}\n" f"\n" f"<i>Выпуск №{month.number}\n</i>" f"\n" f"{month.message}\n"),
            )
        except Exception:  # noqa, pylint: disable=broad-except
            continue


@heroes_regex_matcher("0 8 * * mon")
async def heroes_week_handler(
    api: TelegramBotApi,
) -> None:
    activations = await read_all_heroes_activations()
    week = await get_current_week()
    for activation in activations:
        try:
            await api.send_message(
                chat_id=activation.chat_id,
                text=(f"{MESSAGE_TITLE}\n" f"\n" f"<i>Выпуск №{week.number}\n</i>" f"\n" f"{week.message}\n"),
            )
        except Exception:  # noqa, pylint: disable=broad-except
            continue
