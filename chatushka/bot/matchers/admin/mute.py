from datetime import timedelta
from random import randrange

from chatushka import CommandsMatcher, Message, Telegram
from chatushka.bot.matchers.admin.utils import send_mute_request
from chatushka.bot.settings import get_settings

settings = get_settings()
mute_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)


@mute_matcher("mute", "shutup", "kill")
async def mute_handler(
    api: Telegram,
    message: Message,
    args: list[str],
) -> None:
    restrict_time = timedelta(minutes=randrange(10, 30))
    admins = await api.get_chat_administrators(message.chat.id)

    privileges = None
    for admin in admins:
        if admin.user.id == message.user.id:
            privileges = admin
            break

    if (
        not message.reply_to_message
        or not privileges
        or not privileges.status.CREATOR
        or not privileges.can_restrict_members
    ):
        await send_mute_request(
            api=api,
            message=message,
            initiator=message.user,
            restrict_user=message.user,
            restrict_time=restrict_time,
        )
        return

    try:  # noqa
        restrict_time = timedelta(hours=int(args[0]))
    except (ValueError, IndexError):
        pass

    await send_mute_request(
        api=api,
        message=message,
        initiator=message.user,
        restrict_user=message.reply_to_message.user,
        restrict_time=restrict_time,
    )
