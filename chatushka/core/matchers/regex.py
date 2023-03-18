from logging import getLogger
from re import findall

from chatushka.core.matchers.base import MatcherBase
from chatushka.core.models import MatchedToken, RegexMatchKwargs, Update

logger = getLogger(__name__)


class RegexMatcher(MatcherBase):
    suffix = "regex"

    async def _check(
        self,
        token: str,  # type: ignore
        update: Update,
    ) -> MatchedToken | None:
        if not update.message or not update.message.text:
            return None
        if founded := findall(token, update.message.text):
            kwargs = RegexMatchKwargs(matched=tuple(founded))
            return MatchedToken(
                token=token,
                kwargs=kwargs,
            )
        return None
