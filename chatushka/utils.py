from chatushka.bot_api import TelegramBotAPI


async def check_preconditions(
    api: TelegramBotAPI,
) -> None:
    response = await api.get_me()
    if not response.can_join_groups:
        raise RuntimeError("Talk to @botfather and enable groups access for bot.")
    if not response.can_read_all_group_messages:
        raise RuntimeError("Talk to @botfather and disable the privacy mode.")
