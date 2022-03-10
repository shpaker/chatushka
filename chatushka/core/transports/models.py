from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


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
    first_name: Optional[str]
    last_name: Optional[str]
    can_join_groups: Optional[bool]
    can_read_all_group_messages: Optional[bool]

    @property
    def readable_name(self) -> str:
        return f"{self.first_name}{' '+self.last_name if self.last_name else ''}"


class ChatMemberBase(BaseModel):
    status: ChatMemberStatuses
    user: User
    is_anonymous: Optional[bool] = None
    custom_title: Optional[str] = None


class ChatMemberOwner(ChatMemberBase):
    ...


class ChatMemberAdministrator(ChatMemberBase):
    can_be_edited: Optional[bool]
    can_manage_chat: Optional[bool]
    can_delete_messages: Optional[bool]
    can_manage_voice_chats: Optional[bool]
    can_restrict_members: Optional[bool]
    can_promote_members: Optional[bool]
    can_change_info: Optional[bool]
    can_invite_users: Optional[bool]
    can_post_messages: Optional[bool]
    can_edit_messages: Optional[bool]
    can_pin_messages: Optional[bool]


class Chat(BaseModel):
    id: int
    type: ChatType
    title: Optional[str]


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
    text: Optional[str]
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
        json_decoders = dict(datetime=lambda v: datetime.fromtimestamp(v, tz=timezone.utc))


class Update(BaseModel):
    update_id: int
    message: Optional[Message] = None
    my_chat_member: Optional[MyChatMember] = None


class ChatPermissions(BaseModel):
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    # can_add_web_page_previews: bool
    # can_change_info: bool
    # can_invite_users: bool
    # can_pin_messages: bool
