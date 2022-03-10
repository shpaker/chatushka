from logging import getLogger
from re import findall
from typing import Optional

from chatushka.core.matchers.base import MatcherBase
from chatushka.core.models import MatchedToken, RegexMatchKwargs
from chatushka.core.transports.models import Update

logger = getLogger(__name__)


class RegexMatcher(MatcherBase):

    suffix = "regex"

    async def _check(
        self,
        token: str,  # type: ignore
        update: Update,
    ) -> Optional[MatchedToken]:
        if not update.message or not update.message.text:
            return
        if founded := findall(token, update.message.text):
            kwargs = RegexMatchKwargs(matched=tuple(founded))
            return MatchedToken(
                token=token,
                kwargs=kwargs,
            )
