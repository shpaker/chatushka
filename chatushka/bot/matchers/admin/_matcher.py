from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher

settings = get_settings()
admin_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)
