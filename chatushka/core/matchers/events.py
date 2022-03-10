from logging import getLogger
from typing import Hashable, Iterable, Optional, Union

from chatushka.core.matchers.base import MatcherBase
from chatushka.core.models import EventTypes, MatchedToken
from chatushka.core.transports.models import Update

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
        update: Update,
    ) -> Optional[MatchedToken]:
        return MatchedToken(token=EventTypes.MESSAGE)
