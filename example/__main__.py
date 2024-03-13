import asyncio
import datetime
import os
import random

import chatushka
from example.constants import MAGIC_EIGHT_BALL_CHOICES

bot = chatushka.Chatushka(
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
    user: chatushka.User,
    chat: chatushka.Chat,
) -> None:
    text = f"*USER_ID:* `{user.id}`"
    if user.id != chat.id:
        text += f"\n*CHAT_ID:* `{chat.id}`"
    await api.send_message(
        chat_id=chat.id,
        text=text,
        reply_to_message_id=message.message_id,
        parse_mode="markdown",
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


@bot.event("on_message")
async def welcome_handler(
    api: chatushka.TelegramBotAPI,
    chat: chatushka.Chat,
    message: chatushka.Message,
) -> None:
    await api.send_message(
        chat_id=chat.id,
        text="message",
        reply_to_message_id=message.message_id,
    )


@bot.cmd("suicide", "wtf")
async def suicide_handler(
    api: chatushka.TelegramBotAPI,
    message: chatushka.Message,
) -> None:
    restrict_time = datetime.timedelta(minutes=random.randrange(1, 4 * 60))
    try:
        is_success = await api.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.user.id,
            permissions=chatushka.ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
            ),
            until_date=datetime.datetime.now(
                tz=datetime.timezone.utc,
            ) + restrict_time,
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


if __name__ == "__main__":
    asyncio.run(
        bot.run(),
    )
