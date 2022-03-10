from chatushka.bot.settings import get_settings
from chatushka.core.matchers import ChatUsersMovementsEventsEnum, ChatUsersMovementsMatcher
from chatushka.core.transports.models import Chat, User
from chatushka.core.transports.telegram_bot_api import TelegramBotApi

settings = get_settings()
user_movements_matcher = ChatUsersMovementsMatcher()


@user_movements_matcher(ChatUsersMovementsEventsEnum.CAME)
async def came_handler(
    api: TelegramBotApi,
    chat: Chat,
    user: User,
) -> None:
    text = f'Hi, <a href="tg://user?id={user.id}">{user.readable_name}</a>!'
    await api.send_message(
        chat_id=chat.id,
        text=text,
    )


@user_movements_matcher(ChatUsersMovementsEventsEnum.LEAVE)
async def leave_handler(
    api: TelegramBotApi,
    chat: Chat,
    user: User,
) -> None:
    text = f'Bye, <a href="tg://user?id={user.id}">{user.readable_name}</a>!'
    await api.send_message(
        chat_id=chat.id,
        text=text,
    )
