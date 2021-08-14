from motor.motor_asyncio import AsyncIOMotorCollection

from chatushka.bot.settings import get_settings
from chatushka.core.services.mongodb.utils import get_database

settings = get_settings()


def get_calendar_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db[settings.mongodb.heroes.calendar_collection]


def get_activations_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db[settings.mongodb.heroes.activations_collection]
