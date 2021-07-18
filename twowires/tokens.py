from typing import List

from twowires.models import telegram_types
from twowires.telegram import send_message


async def check_tokens(
    updates: List[telegram_types.Update]
):
    for update in updates:
        if update.message.text == "дурак":
            await send_message(
                chat_id=update.message.chat.id,
                text="сам дурак",
                reply_to_message_id=update.message.message_id,
            )
