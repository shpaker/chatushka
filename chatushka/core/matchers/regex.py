from logging import getLogger
from re import findall
from typing import Optional

from chatushka.core.matchers.base import MatcherBase
from chatushka.core.models import MatchedToken, RegexMatchKwargs
from chatushka.core.transports.models import Message

logger = getLogger(__name__)


class RegexMatcher(MatcherBase):

    suffix = "regex"

    # def _cast_token(
    #     self,
    #     token: str,
    # ) -> Union[Hashable, Iterable[Hashable]]:
    #     return compile(token)

    async def _check(
        self,
        token: str,  # type: ignore
        message: Message,
    ) -> Optional[MatchedToken]:
        if founded := findall(token, message.text):
            kwargs = RegexMatchKwargs(matched=tuple(founded))
            return MatchedToken(
                token=token,
                kwargs=kwargs,
            )
