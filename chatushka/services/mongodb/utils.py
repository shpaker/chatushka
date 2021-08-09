from typing import Any, Dict, List, Optional, Tuple

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from chatushka.services.mongodb.wrapper import MongoDBWrapper
from chatushka.settings import get_settings

settings = get_settings()


def get_mongodb_client() -> AsyncIOMotorClient:
    return MongoDBWrapper().client


def get_database() -> AsyncIOMotorCollection:
    client = get_mongodb_client()
    return client[settings.mongodb.database]


async def mongodb_paginated_find(
    collection: AsyncIOMotorClient,
    query: Optional[Dict[str, Any]],
    page: int,
    per_page: int,
    sort: Optional[List[Tuple[str, int]]] = None,
    projection: Optional[Dict[str, int]] = None,
) -> List[Dict[str, Any]]:
    cursor = collection.find(query, sort=sort, projection=projection)
    cursor.skip(page * per_page).limit(per_page)
    return [doc async for doc in cursor]
