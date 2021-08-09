from motor.motor_asyncio import AsyncIOMotorCollection

from chatushka.services.mongodb.utils import get_database
from chatushka.settings import get_settings

settings = get_settings()


def get_calendar_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db[settings.samples.heroes.calendar_collection]


def get_activations_collection() -> AsyncIOMotorCollection:
    db = get_database()
    return db[settings.samples.heroes.activations_collection]
