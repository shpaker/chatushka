from logging import getLogger
from re import compile, findall
from typing import Optional, Union, Iterable, Hashable

from twowires.matchers.base import MatcherBase
from twowires.matchers.types import MatchedToken, RegexMatchKwargs
from twowires.transports.models import Message

logger = getLogger(__name__)


class RegexMatcher(MatcherBase):

    suffix = "regex"

    async def _cast_token(
        self,
        token: str,
    ) -> Union[Hashable, Iterable[Hashable]]:
        return compile(token)

    async def _check(
        self,
        token: str,
        message: Message,
    ) -> Optional[MatchedToken]:
        if founded := findall(token, message.text):
            kwargs = RegexMatchKwargs(founded=tuple(founded))
            return MatchedToken(
                token=token,
                kwargs=kwargs,
            )
