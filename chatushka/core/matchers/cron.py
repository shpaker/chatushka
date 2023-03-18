from contextlib import suppress
from logging import getLogger

from chatushka.core.matchers.base import MatcherBase

with suppress(ImportError):
    from aiocron import crontab


logger = getLogger(__name__)


class CronMatcher(MatcherBase):
    async def init(self) -> None:
        for token, handlers in self.handlers.items():
            for handler in handlers:
                crontab(token, func=handler)
