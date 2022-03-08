from chatushka.bot.matchers.admin.mute import mute_matcher
from chatushka.bot.matchers.admin.pin import pin_matcher
from chatushka.bot.settings import get_settings
from chatushka.core.matchers import CommandsMatcher

settings = get_settings()
admin_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)
admin_matcher.add_matcher(
    mute_matcher,
    pin_matcher,
)

__all__ = ("admin_matcher",)
