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
        if update.message and update.message.new_chat_members:
            return MatchedToken(token=ChatUsersMovementsEventsEnum.CAME)
