from logging import getLogger

from aiocron import crontab

from twowires.matchers.base import MatcherBase

logger = getLogger(__name__)


class CronMatcher(MatcherBase):
    def init(self):
        for token, handler in self.handlers.items():
            crontab(token, func=handler)
