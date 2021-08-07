from logging import getLogger
from typing import Hashable, Iterable, Optional, Union

from chatushka.matchers.base import MatcherBase
from chatushka.transports.models import Message
from chatushka.types import EventTypes, MatchedToken

logger = getLogger(__name__)


class EventsMatcher(MatcherBase):
    def _cast_token(
        self,
        token: str,
    ) -> Union[str, Iterable[str]]:
        if isinstance(token, str):
            return EventTypes[token.upper()]
        return token

    async def _check(
        self,
        token: Hashable,
        message: Message,
    ) -> Optional[MatchedToken]:
        return MatchedToken(token=EventTypes.MESSAGE)
