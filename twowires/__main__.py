from logging import basicConfig, getLogger, INFO, DEBUG
from asyncio import run
from twowires import telegram
from twowires.bot import TwoWiresBot
from twowires.settings import get_settings

logger = getLogger()
settings = get_settings()


def config_logger():
    log_level = DEBUG if settings.debug else INFO
    basicConfig(level=log_level)


if __name__ == "__main__":
    bot = TwoWiresBot()
    bot.add_event_handler("startup", config_logger)
    bot.add_event_handler("startup", telegram.check_preconditions)
    run(bot.serve())
