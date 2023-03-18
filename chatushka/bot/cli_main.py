from asyncio import run
from logging import DEBUG, INFO, WARNING, basicConfig, getLogger

from chatushka import Chatushka
from chatushka.bot.matchers.admin import admin_matcher
from chatushka.bot.matchers.users import user_matcher
from chatushka.bot.settings import get_settings

logger = getLogger()
settings = get_settings()


def make_bot(
    token: str,
    debug: bool,
) -> Chatushka:
    bot = Chatushka(token=token, debug=debug)
    bot.add_matcher(
        admin_matcher,
        user_matcher,
    )
    return bot


def cli_main(
    token: str,
    debug: bool,
) -> None:
    basicConfig(level=DEBUG if debug else INFO)
    getLogger("httpx").setLevel(WARNING)
    logger.debug("Debug mode is on".upper())
    bot = make_bot(token, debug)
    run(bot.serve())
