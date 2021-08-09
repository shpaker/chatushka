from asyncio import run
from logging import DEBUG, INFO, WARNING, basicConfig, getLogger

from chatushka import Chatushka
from chatushka.matchers import CommandsMatcher, RegexMatcher
from chatushka.samples.handlers.eight_ball import eight_ball_answer_handler, eight_ball_handler
from chatushka.samples.handlers.helpers import mute_handler, suicide_handler
from chatushka.samples.handlers.id import user_id_handler
from chatushka.samples.handlers.jokes import jokes_handler
from chatushka.samples.matchers.heroes.matchers import add_heroes_matchers
from chatushka.services.mongodb.wrapper import MongoDBWrapper
from chatushka.settings import get_settings

logger = getLogger()
settings = get_settings()


def make_regex_matcher():
    matcher = RegexMatcher()
    matcher.add_handler(r"\?", eight_ball_answer_handler)
    return matcher


def make_commands_matcher():
    matcher = CommandsMatcher(
        prefixes=settings.command_prefixes,
        postfixes=settings.command_postfixes,
        allow_raw=True,
    )
    matcher.add_handler("id", user_id_handler)
    matcher.add_handler("joke", jokes_handler)
    matcher.add_handler(("8ball", "ball8", "b8", "8b"), eight_ball_handler)
    return matcher


def make_sensitive_matcher():
    matcher = CommandsMatcher(
        prefixes=settings.command_prefixes,
        postfixes=settings.command_postfixes,
    )
    matcher.add_handler(("suicide", "wtf"), suicide_handler)
    return matcher


def make_privilege_matcher():
    matcher = CommandsMatcher(
        prefixes=settings.command_prefixes,
        postfixes=settings.command_postfixes,
    )
    matcher.add_handler("mute", mute_handler)
    return matcher


def make_bot() -> Chatushka:
    instance = Chatushka(token=settings.token, debug=settings.debug)
    wrapper = MongoDBWrapper()
    wrapper.add_event_handlers(instance)
    add_heroes_matchers(instance)
    instance.add_matchers(
        make_commands_matcher(),
        make_sensitive_matcher(),
        make_privilege_matcher(),
        make_regex_matcher(),
    )
    return instance


def main():
    basicConfig(level=DEBUG if settings.debug else INFO)
    logger.debug("Debug mode is on".upper())
    getLogger("httpx").setLevel(WARNING)
    bot = make_bot()
    run(bot.serve())


if __name__ == "__main__":
    main()
