from chatushka.bot.settings import get_settings
from chatushka.core.matchers import ChatUsersMovementsEventsEnum, ChatUsersMovementsMatcher
from chatushka.core.transports.models import Message
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

settings = get_settings()
welcoming_matcher = ChatUsersMovementsMatcher()


@welcoming_matcher(ChatUsersMovementsEventsEnum.CAME, include_in_help=False)
async def came_handler(
    api: TelegramBotApi,
    message: Message,
) -> None:
    for user in message.new_chat_members:
        text = f'Привет, <a href="tg://user?id={user.id}">{user.readable_name}</a>!'
        await api.send_message(
            chat_id=message.chat.id,
            text=text,
        )
