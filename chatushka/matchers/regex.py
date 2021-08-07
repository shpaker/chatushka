from logging import getLogger
from re import findall
from typing import Optional

from chatushka.matchers.base import MatcherBase
from chatushka.transports.models import Message
from chatushka.models import MatchedToken, RegexMatchKwargs

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
