from chatushka.samples.heroes.cruds.activations import set_heroes_activation, read_all_heroes_activations
from chatushka.samples.heroes.cruds.months import get_current_month
from chatushka.samples.heroes.cruds.weeks import get_current_week
from chatushka.samples.heroes.utils import extract_state
from chatushka.transports.models import Message
from chatushka.transports.telegram_bot_api import TelegramBotApi

MESSAGE_TITLE = "✨💫✨ <b>ГЕРОЙСКИЙ КАЛЕНДАРЬ</b> 💫✨💫"


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
        "🙂 Подписка на периодическое издание \"Геройский календарь\" оформлена"
    ) if state else (
        "😏 Вы отписались от периодического издания \"Геройский календарь\""
    )
    await api.send_message(
        chat_id=message.chat.id,
        text=state_msg,
        reply_to_message_id=message.message_id,
    )


async def heroes_month_handler(
    api: TelegramBotApi,
) -> None:
    activations = await read_all_heroes_activations()
    month = await get_current_month()
    for activation in activations:
        try:
            await api.send_message(
                chat_id=activation.chat_id,
                text=(
                    f"{MESSAGE_TITLE}\n"
                    f"\n"
                    f"<i>Выпуск №{month.number}\n</i>"
                    f"\n"
                    f"{month.message}\n"
                ),
            )
        except Exception:  # noqa, pylint: disable=too-bare-exception
            continue


async def heroes_week_handler(
    api: TelegramBotApi,
) -> None:
    activations = await read_all_heroes_activations()
    week = await get_current_week()
    for activation in activations:
        try:
            await api.send_message(
                chat_id=activation.chat_id,
                text=(
                    f"{MESSAGE_TITLE}\n"
                    f"\n"
                    f"<i>Выпуск №{week.number}\n</i>"
                    f"\n"
                    f"{week.message}\n"
                ),
            )
        except Exception:  # noqa, pylint: disable=too-bare-exception
            continue
