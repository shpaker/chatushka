from asyncio import run
from logging import DEBUG, INFO, WARNING, basicConfig, getLogger

from click import command, option

from chatushka import ChatushkaBot
from chatushka.bot.matchers import eight_ball_matchers, helpers_matcher, heroes_matchers, jokes_matcher, suicide_matcher
from chatushka.bot.settings import get_settings
from chatushka.core.services.mongodb.wrapper import MongoDBWrapper

logger = getLogger()
settings = get_settings()


def make_bot(
    token: str,
    debug: bool,
) -> ChatushkaBot:
    instance = ChatushkaBot(token=token, debug=debug)
    wrapper = MongoDBWrapper()
    wrapper.add_event_handlers(instance)

    instance.add_matchers(
        jokes_matcher,
        *eight_ball_matchers,
        helpers_matcher,
        *heroes_matchers,
        suicide_matcher,
    )

    instance.add_matchers()
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
