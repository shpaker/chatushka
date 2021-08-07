from logging import getLogger
from typing import Union, Iterable, Optional, Hashable

from twowires.matchers.base import MatcherBase
from twowires.matchers.types import MatchedToken, BotEvents
from twowires.transports.models import Message

logger = getLogger(__name__)


class EventsMatcher(MatcherBase):

    suffix = "event"

    async def _cast_token(
        self,
        token: str,
    ) -> Union[str, Iterable[str]]:
        if isinstance(token, str):
            return BotEvents[token.upper()]
        return token

    async def _check(
        self,
        token: Hashable,
        message: Message,
    ) -> Optional[MatchedToken]:
        return MatchedToken(token=BotEvents.ON_MESSAGE)
