from datetime import datetime, timezone
from enum import Enum
from typing import Optional, TypedDict

from pydantic import BaseModel, Field

from chatushka.samples.matchers.heroes.utils import get_month_message, get_week_message


class CalendarTypes(str, Enum):
    MONTH = "month"
    WEEK = "week"


class CalendarMeta(BaseModel):
    type: CalendarTypes
    message: str
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    number: int = Field(1, ge=1)


class CalendarWeekModel(CalendarMeta):
    type: CalendarTypes = CalendarTypes.WEEK
    message: str = Field(default_factory=get_week_message)


class CalendarMonthModel(CalendarMeta):
    type: CalendarTypes = CalendarTypes.MONTH
    message: str = Field(default_factory=get_month_message)


class HeroesActivationMeta(TypedDict):
    chat_title: str
    activated_by: str


class HeroesActivationUpdatableModel(BaseModel):
    activated_by_id: int
    meta: Optional[HeroesActivationMeta]
    state: bool = True
    activated_ts: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))


class HeroesActivationModel(HeroesActivationUpdatableModel):
    chat_id: int
