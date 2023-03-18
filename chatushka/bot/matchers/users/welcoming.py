from chatushka import ChatUsersMovementsEventsEnum, ChatUsersMovementsMatcher, Message, Telegram
from chatushka.bot.settings import get_settings

settings = get_settings()
welcoming_matcher = ChatUsersMovementsMatcher()


@welcoming_matcher(ChatUsersMovementsEventsEnum.CAME, include_in_help=False)
async def came_handler(
    api: Telegram,
    message: Message,
) -> None:
    for user in message.new_chat_members:
        text = f'Привет, <a href="tg://user?id={user.id}">{user.readable_name}</a>!'
        await api.send_message(
            chat_id=message.chat.id,
            text=text,
        )
