import asyncio
import contextlib
import os
import random

import chatushka
from example.constants import MAGIC_EIGHT_BALL_CHOICES

bot = chatushka.ChatushkaBot(
    token=os.environ["CHATUSHKA_TOKEN"],
    cmd_prefixes=("!", "/"),
)


@bot.cmd("8ball", "ball8", "b8", "8b")
async def magic_ball_cmd_handler(
    api: chatushka.TelegramBotAPI,
    message: chatushka.Message,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text=random.choice(MAGIC_EIGHT_BALL_CHOICES),
        reply_to_message_id=message.message_id,
    )


@bot.regex(r"\?", chance_rate=0.4)
async def magic_ball_regex_handler(
    api: chatushka.TelegramBotAPI,
    message: chatushka.Message,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text=random.choice(MAGIC_EIGHT_BALL_CHOICES),
        reply_to_message_id=message.message_id,
    )


@bot.cmd("lukashenko", "luk", "lag")
async def luk_handler(
    api: chatushka.TelegramBotAPI,
    message: chatushka.Message,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text=random.choice(MAGIC_EIGHT_BALL_CHOICES),
        reply_to_message_id=message.message_id,
    )


@bot.cmd("id")
async def id_handler(
    api: chatushka.TelegramBotAPI,
    message: chatushka.Message,
) -> None:
    admins = []
    with contextlib.suppress(chatushka.ChatushkaResponseError):
        admins = await api.get_chat_administrators(
            chat_id=message.chat.id,
        )
    line_tmpl = "{id_type}: <pre>{id_value}</pre>"
    ids = {"user_id": message.user.id}
    for admin in admins:
        if admin.user.id == message.user.id:
            ids = ids | {"chat_id": message.chat.id}
    text = "\n".join(
        [
            line_tmpl.format(id_type=id_type, id_value=id_value)
            for id_type, id_value in ids.items()
        ]
    )
    await api.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_to_message_id=message.message_id,
    )


@bot.cmd("ping")
async def ping_handler(
    api: chatushka.TelegramBotAPI,
    message: chatushka.Message,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text="pong",
        reply_to_message_id=message.message_id,
    )


if __name__ == "__main__":
    asyncio.run(bot.run())
