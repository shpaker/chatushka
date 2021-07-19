from asyncio import run
from logging import DEBUG, INFO, basicConfig, getLogger

from twowires.bot import TwoWiresBot
from twowires.models.telegram_types import Message, Update
from twowires.settings import get_settings
from twowires.telegram import get_me, send_message

logger = getLogger()
settings = get_settings()
bot = TwoWiresBot()


@bot.on_event("startup")
def config_logger() -> None:
    log_level = DEBUG if settings.debug else INFO
    basicConfig(level=log_level)


@bot.on_event("startup")  # type: ignore
async def check_preconditions() -> None:
    response = await get_me()
    if not response.can_join_groups:
        raise RuntimeError("Talk to @botfather and enable groups access for bot.")
    if not response.can_read_all_group_messages:
        raise RuntimeError("Talk to @botfather and disable the privacy mode.")


@bot.on_event("on_message")  # type: ignore
def on_message(message: Message) -> None:
    print(message.dict())


@bot.on_message(r"\becho\b")  # type: ignore
async def on_message_echo(
    update: Update,
) -> None:
    await send_message(
        chat_id=update.message.chat.id,
        text="foo",
        reply_to_message_id=update.message.message_id,
    )


if __name__ == "__main__":
    run(bot.serve())
