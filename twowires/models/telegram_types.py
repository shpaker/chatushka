from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ChatType(str, Enum):
    GROUP = "group"
    SUPERGROUP = "supergroup"


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: Optional[str]
    last_name: Optional[str]
    can_join_groups: Optional[bool]
    can_read_all_group_messages: Optional[bool]

    @property
    def readable_name(self):
        return f"{self.first_name}{' '+self.last_name if self.last_name else ''}"


class Chat(BaseModel):
    id: int
    type: ChatType
    title: Optional[str]


class Message(BaseModel):
    message_id: int
    user: User = Field(..., alias="from")
    chat: Chat
    text: str


class Update(BaseModel):
    update_id: int
    message: Message
