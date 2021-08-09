from typing import Optional

from pymongo.results import InsertOneResult, UpdateResult

from chatushka.samples.matchers.heroes.models import (
    HeroesActivationMeta,
    HeroesActivationModel,
    HeroesActivationUpdatableModel,
)
from chatushka.samples.matchers.heroes.mongodb import get_activations_collection
from chatushka.transports.models import Chat, User


async def create_heroes_activation(
    user: User,
    chat: Chat,
    state: bool,
) -> Optional[HeroesActivationModel]:
    collection = get_activations_collection()
    data = HeroesActivationModel(
        chat_id=chat.id,
        activated_by_id=user.id,
        meta=HeroesActivationMeta(
            chat_title=chat.title,
            activated_by=user.readable_name,
        ),
        state=state,
    )
    _: InsertOneResult = await collection.insert_one(data.dict())
    return data


async def update_heroes_activation(
    user: User,
    chat: Chat,
    state: bool,
) -> Optional[HeroesActivationModel]:
    collection = get_activations_collection()
    data = HeroesActivationUpdatableModel(
        activated_by_id=user.id,
        meta=HeroesActivationMeta(
            chat_title=chat.title,
            activated_by=user.readable_name,
        ),
        state=state,
    )
    res: UpdateResult = await collection.update_one(
        dict(chat_id=chat.id),
        {
            "$set": data.dict(),
        },
    )
    if not res.modified_count:
        return None
    return HeroesActivationModel(chat_id=chat.id, **data.dict())


async def set_heroes_activation(
    user: User,
    chat: Chat,
    state: bool,
) -> HeroesActivationModel:
    if data := await update_heroes_activation(user, chat, state):
        return data
    await create_heroes_activation(user, chat, state)


async def read_heroes_activation(
    chat: Chat,
) -> Optional[HeroesActivationModel]:
    collection = get_activations_collection()
    doc = await collection.find_one(dict(chat_id=chat.id))
    if not doc:
        return
    return HeroesActivationModel(**doc)


async def read_all_heroes_activations() -> list[HeroesActivationModel]:
    col = get_activations_collection()
    cursor = col.find(dict())
    return list(HeroesActivationModel(**doc) async for doc in cursor)
