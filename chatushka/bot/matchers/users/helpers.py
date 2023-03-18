from chatushka import CommandsMatcher, Message, Telegram
from chatushka.bot.settings import get_settings

settings = get_settings()
helpers_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)


@helpers_matcher("id")
async def id_handler(
    api: Telegram,
    message: Message,
) -> None:
    admins = await api.get_chat_administrators(message.chat.id)
    line_tmpl = "{id_type}: <pre>{id_value}</pre>"
    ids = {"user_id": message.user.id}
    for admin in admins:
        if admin.user.id == message.user.id:
            ids = ids | {"chat_id": message.chat.id}
    text = "\n".join([line_tmpl.format(id_type=id_type, id_value=id_value) for id_type, id_value in ids.items()])
    await api.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_to_message_id=message.message_id,
    )


@helpers_matcher("ping", "пинг")
async def ping_handler(
    api: Telegram,
    message: Message,
) -> None:
    answer = "pong" if "ping" in message.text else "понг"
    await api.send_message(
        chat_id=message.chat.id,
        text=answer,
        reply_to_message_id=message.message_id,
    )
