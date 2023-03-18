from collections.abc import Hashable, Iterable
from logging import getLogger

from chatushka.core.models import EventTypes, MatchedToken
from chatushka.core.telegram.models import Update
from chatushka.matchers.base import MatcherBase

logger = getLogger(__name__)


class EventsMatcher(MatcherBase):
    def _cast_token(
        self,
        token: str,
    ) -> str | Iterable[str]:
        if isinstance(token, str):
            return EventTypes[token.upper()]
        return token

    async def _check(
        self,
        token: Hashable,
        update: Update,
    ) -> MatchedToken | None:
        return MatchedToken(token=EventTypes.MESSAGE)