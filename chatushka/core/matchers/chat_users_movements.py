from enum import Enum, auto, unique
from logging import getLogger
from typing import Hashable, Optional, Union

from chatushka.core.matchers.base import MatcherBase
from chatushka.core.models import MatchedToken
from chatushka.core.transports.models import Update

logger = getLogger(__name__)


@unique
class ChatUsersMovementsEventsEnum(Enum):
    CAME = auto()
    LEAVE = auto()
    # CHANGE_STATE = auto()


class ChatUsersMovementsMatcher(MatcherBase):
    def _cast_token(
        self,
        token: Union[str, ChatUsersMovementsEventsEnum],
    ) -> ChatUsersMovementsEventsEnum:
        if isinstance(token, str):
            return ChatUsersMovementsEventsEnum[token.upper()]
        return token

    async def _check(
        self,
        token: Hashable,
        update: Update,
    ) -> Optional[MatchedToken]:
        pass
        # words = tuple(word for word in message.text.split(" ") if word)
        # for i, word in enumerate(words):
        #     if not self._case_sensitive:
        #         word = word.lower()
        #     if token == word:
        #         return MatchedToken(
        #             token=token,
        #             args=tuple(words[i + 1 :]),  # noqa
        #         )
