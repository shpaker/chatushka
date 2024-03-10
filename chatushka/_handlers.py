from contextlib import suppress

from chatushka._errors import ChatushkaResponseError
from chatushka._models import Message
from chatushka._transport import TelegramBotAPI


async def id_handler(
    api: TelegramBotAPI,
    message: Message,
) -> None:
    admins = []
    with suppress(ChatushkaResponseError):
        admins = await api.get_chat_administrators(
            chat_id=message.chat.id,
        )
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


async def ping_handler(
    api: TelegramBotAPI,
    message: Message,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text="pong",
        reply_to_message_id=message.message_id,
    )
