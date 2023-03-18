from chatushka import CommandsMatcher
from chatushka.bot.matchers.users.bobuk_jokes import jokes_matcher
from chatushka.bot.matchers.users.eight_ball import eight_ball_matcher
from chatushka.bot.matchers.users.helpers import helpers_matcher
from chatushka.bot.matchers.users.lukashenko import lukashenko_matcher
from chatushka.bot.matchers.users.philosophy import philosophy_matcher
from chatushka.bot.matchers.users.suicide import suicide_matcher
from chatushka.bot.matchers.users.welcoming import welcoming_matcher
from chatushka.bot.settings import get_settings

settings = get_settings()
user_matcher = CommandsMatcher(
    prefixes=settings.command_prefixes,
    postfixes=settings.command_postfixes,
)
user_matcher.add_matcher(
    jokes_matcher,
    eight_ball_matcher,
    helpers_matcher,
    suicide_matcher,
    lukashenko_matcher,
    welcoming_matcher,
    philosophy_matcher,
)

__all__ = ("user_matcher",)
