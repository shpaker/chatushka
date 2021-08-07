from logging import getLogger

from aiocron import crontab

from chatushka.matchers.base import MatcherBase

logger = getLogger(__name__)


class CronMatcher(MatcherBase):
    async def init(self) -> None:
        for token, handlers in self.handlers.items():
            for handler in handlers:
                crontab(token, func=handler)
