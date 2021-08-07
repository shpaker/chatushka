from logging import getLogger

from aiocron import crontab

from twowires.matchers.base import MatcherBase

logger = getLogger(__name__)


class CronMatcher(MatcherBase):
    async def init(self):
        for token, handlers in self.handlers.items():
            for handler in handlers:
                crontab(token, func=handler)
