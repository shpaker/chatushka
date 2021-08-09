from chatushka import Chatushka
from chatushka.matchers import CommandsMatcher, RegexMatcher
from chatushka.samples.heroes.handlers import activate_heroes_handler, heroes_week_handler, heroes_month_handler
from chatushka.settings import get_settings

settings = get_settings()


def add_heroes_matchers(
    bot: Chatushka,
) -> None:
    commands = CommandsMatcher(
        prefixes=settings.command_prefixes,
        postfixes=settings.command_postfixes,
    )
    regex = RegexMatcher()
    commands.add_handler(("homm", "heroes"), activate_heroes_handler)
    regex.add_handler("0 8 * * mon", heroes_week_handler)
    regex.add_handler("2 4 1 * *", heroes_month_handler)
    bot.add_matchers(regex, commands)
