from collections.abc import Callable, Coroutine, Hashable
from datetime import UTC, datetime
from enum import Enum, auto, unique
from typing import Any, NamedTuple, Optional, TypedDict, Union

from pydantic import BaseModel, Field

# pylint: disable=invalid-name
HANDLER_TYPING = Union[
    Callable[[Any], None],
    Callable[[Any], Coroutine[Any, Any, Any]],
]


class ChatType(str, Enum):
    GROUP = "group"
    SUPERGROUP = "supergroup"
    PRIVATE = "private"


class ChatMemberStatuses(str, Enum):
    MEMBER = "member"
    CREATOR = "creator"
    ADMINISTRATOR = "administrator"
    LEFT = "left"
    KICKED = "kicked"
    RESTRICTED = "restricted"


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    can_join_groups: bool | None
    can_read_all_group_messages: bool | None

    @property
    def readable_name(self) -> str:
        return f"{self.first_name}{' '+self.last_name if self.last_name else ''}"


class ChatMemberBase(BaseModel):
    status: ChatMemberStatuses
    user: User
    is_anonymous: bool | None = None
    custom_title: str | None = None


class ChatMemberOwner(ChatMemberBase):
    ...


class ChatMemberAdministrator(ChatMemberBase):
    can_be_edited: bool | None
    can_manage_chat: bool | None
    can_delete_messages: bool | None
    can_manage_voice_chats: bool | None
    can_restrict_members: bool | None
    can_promote_members: bool | None
    can_change_info: bool | None
    can_invite_users: bool | None
    can_post_messages: bool | None
    can_edit_messages: bool | None
    can_pin_messages: bool | None


class Chat(BaseModel):
    id: int
    type: ChatType
    title: str | None


class NewChatMember(
    ChatMemberAdministrator,
):
    ...


class OldChatMember(
    ChatMemberAdministrator,
):
    ...


class Message(BaseModel):
    message_id: int
    user: User = Field(..., alias="from")
    chat: Chat
    text: str | None
    reply_to_message: Optional["Message"] = None
    new_chat_members: list[User] = Field(default_factory=list)


Message.update_forward_refs()


class MyChatMember(BaseModel):
    chat: Chat
    user: User = Field(..., alias="from")
    date: datetime
    old_chat_member: OldChatMember
    new_chat_member: NewChatMember

    class Config:
        json_decoders = {"datetime": lambda v: datetime.fromtimestamp(v, tz=UTC)}


class Update(BaseModel):
    update_id: int
    message: Message | None = None
    my_chat_member: MyChatMember | None = None


class ChatPermissions(BaseModel):
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool


class RegexMatchKwargs(TypedDict):
    matched: tuple[str, ...]


class MatchedToken(NamedTuple):
    token: Hashable
    args: tuple[str, ...] = ()
    kwargs: dict[str, Any] = {}


@unique
class EventTypes(Enum):
    STARTUP = auto()
    SHUTDOWN = auto()
    MESSAGE = auto()
