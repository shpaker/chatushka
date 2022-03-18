from asyncio import run
from logging import DEBUG, INFO, WARNING, basicConfig, getLogger

from click import command, option

from chatushka import ChatushkaBot
from chatushka.bot.matchers import (
    admin_matcher,
    eight_ball_matcher,
    helpers_matcher,
    jokes_matcher,
    lukashenko_matcher,
    philosophy_matcher,
    suicide_matcher,
    welcoming_matcher,
)
from chatushka.bot.settings import get_settings

logger = getLogger()
settings = get_settings()


def make_bot(
    token: str,
    debug: bool,
) -> ChatushkaBot:
    instance = ChatushkaBot(token=token, debug=debug)
    instance.add_matcher(
        admin_matcher,
        jokes_matcher,
        eight_ball_matcher,
        helpers_matcher,
        suicide_matcher,
        lukashenko_matcher,
        welcoming_matcher,
        philosophy_matcher,
    )
    return instance


@command()
@option(
    "--token",
    "-t",
    required=True,
)
@option(
    "--debug/--no-debug",
    is_flag=True,
)
def cli_main(
    token: str,
    debug: bool,
) -> None:
    basicConfig(level=DEBUG if debug else INFO)
    getLogger("httpx").setLevel(WARNING)
    logger.debug("Debug mode is on".upper())
    bot = make_bot(token, debug)
    run(bot.serve())
