from datetime import datetime, timezone
from random import randrange, choice
from typing import Optional, TypedDict

from pydantic import BaseModel, Field
from pymongo.results import InsertOneResult, UpdateResult

from chatushka import Chatushka
from chatushka.protocols import MatcherProtocol
from chatushka.services.mongodb.depends import get_homm_collection
from chatushka.transports.models import Message, Chat, User
from chatushka.transports.telegram_bot_api import TelegramBotApi

BOOL_TRUE_VALUES = ("+", "y", "yes", "true", "on")
BOOL_FALSE_VALUES = ("-", "n", "no", "false", "off")

REGULAR_WEEK_TEMPLATE = (
    "Астрологи объявляют неделю <b>{beast}</b>.\n"
    "Население всех жилищ возросло."
)
SPECIAL_WEEK_TEMPLATE = (
    "Астрологи объявляют, что этой неделе покровительствует сила <b>{beasts}</b>.\n"
    "Популяция <b>{beasts}</b> +5.\n"
    "Население всех жилищ возросло."
)
PLAGUE_MONTH_MESSAGE = "Астрологи объявляют месяц ЧУМЫ! Население всех жилищ уменьшилось вдвое."
REGULAR_MONTH_MESSAGE = "Астрологи объявляют месяц <b>{unit}</b>. Население всех жилищ возросло."
SPECIAL_MONTH_MESSAGE = (
    "Астрологи объявляют, что этому месяцу покровительствует сила <b>{unit}</b>.\n"
    "Популяция <b>{unit}</b> удваивается!\n"
    "Население всех жилищ возросло"
)
REGULAR_WEEK_UNIT = (
    "белки",
    "кролика",
    "суслика",
    'барсука',
    "крысы",
    "орла",
    "горностая",
    "ворона",
    "мангуста",
    "собаки",
    "муравьеда",
    "ящерицы",
    "черепахи",
    "дикобраза",
    "кондора",
)

# https://homm3sod.ru/units/
PLAYABLE_UNITS = (
    "копейщиков",
    "алебардщиков",
    "лучников",
    "стрелоков",
    "грифонов",
    "королевский грифонов",
    "крестоносецев",
    "монахов",
    'фанатиков',
    "кавалеристов",
    "чемпионов",
    "ангелов",
    "архангелов",
)
REGULAR_MONTH_UNIT = (
    "кузнечика",
    "муравья",
    "стрекозы",
    "паука",
    "бабочки",
    "шмеля",
    "цикады",
    "земляного червя",
    "шершня",
    "жука",
)


def _get_regular_week() -> str:
    beast = choice(REGULAR_WEEK_UNIT)
    return REGULAR_WEEK_TEMPLATE.format(beast=beast)


def _get_monster_week() -> str:
    unit = choice(PLAYABLE_UNITS)
    return SPECIAL_WEEK_TEMPLATE.format(beasts=unit)


def get_week_name() -> str:
    is_regular_week = randrange(4) != 0
    return _get_regular_week() if is_regular_week else _get_monster_week()


def _get_regular_month() -> str:
    unit = choice(REGULAR_MONTH_UNIT)
    return REGULAR_MONTH_MESSAGE.format(unit=unit)


def _get_unit_month() -> str:
    unit = choice(REGULAR_MONTH_UNIT)
    return SPECIAL_MONTH_MESSAGE.format(unit=unit)


def get_month_name():
    random_int = randrange(10)
    if random_int < 5:
        return _get_regular_month()
    if random_int == 5:
        return PLAGUE_MONTH_MESSAGE
    return _get_unit_month()


class HommRecordMeta(TypedDict):
    chat_title: str
    activated_by: str


class HommRecordUpdatable(BaseModel):
    activated_by_id: int
    meta: Optional[HommRecordMeta]
    state: bool = True
    activated_ts: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))


class HommRecord(HommRecordUpdatable):
    chat_id: int


async def create_homm_activation(
    user: User,
    chat: Chat,
    state: bool,
) -> Optional[HommRecord]:
    collection = get_homm_collection()
    data = HommRecord(
        chat_id=chat.id,
        activated_by_id=user.id,
        meta=HommRecordMeta(
            chat_title=chat.title,
            activated_by=user.readable_name,
        ),
        state=state,
    )
    _: InsertOneResult = await collection.insert_one(data.dict())
    return data


async def update_homm_activation(
    user: User,
    chat: Chat,
    state: bool,
) -> Optional[HommRecord]:
    collection = get_homm_collection()
    data = HommRecordUpdatable(
        activated_by_id=user.id,
        meta=HommRecordMeta(
            chat_title=chat.title,
            activated_by=user.readable_name,
        ),
        state=state,
    )
    res: UpdateResult = await collection.update_one(
        {
            "chat_id": chat.id,
        },
        {
            "$set": data.dict(),
        },
    )
    if not res.modified_count:
        return None
    return HommRecord(chat_id=chat.id, **data.dict())


async def ensure_homm_activation(
    user: User,
    chat: Chat,
    state: bool,
) -> HommRecord:
    if data := await update_homm_activation(user, chat, state):
        return data
    await create_homm_activation(user, chat, state)


async def read_homm_activation(
    chat: Chat,
) -> Optional[HommRecord]:
    collection = get_homm_collection()
    doc = await collection.find_one(dict(chat_id=chat.id))
    if not doc:
        return
    return HommRecord(**doc)


async def read_all_homm_activations() -> list[HommRecord]:
    col = get_homm_collection()
    cursor = col.find(dict())
    return list(HommRecord(**doc) async for doc in cursor)


def extract_state(value: str) -> bool:
    if value in BOOL_FALSE_VALUES:
        return False
    return True


async def activate_homm_handler(
    api: TelegramBotApi,
    message: Message,
    args: list[str],
) -> None:
    state = True if not args else extract_state(args[0])
    await ensure_homm_activation(
        user=message.user,
        chat=message.chat,
        state=state,
    )
    state_msg = "Активировано" if state else "Деактивировано"
    await api.send_message(
        chat_id=message.chat.id,
        text=f"{state_msg.capitalize()} отслеживание героиского календаря",
        reply_to_message_id=message.message_id,
    )


def add_homm_handlers(
    matcher: MatcherProtocol,
) -> None:
    matcher.add_handler("homm", activate_homm_handler)
