from enum import Enum, auto, unique
from logging import getLogger
from typing import Hashable, Optional, Union

from chatushka.core.matchers.base import MatcherBase
from chatushka.core.models import MatchedToken
from chatushka.core.transports.models import ChatMemberStatuses, Update

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
        if (
            update.my_chat_member is not None
            and update.my_chat_member.new_chat_member.status is ChatMemberStatuses.MEMBER
        ):
            return MatchedToken(token=ChatUsersMovementsEventsEnum.CAME)
