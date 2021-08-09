from datetime import datetime, timezone, timedelta

from pymongo.results import InsertOneResult, UpdateResult

from chatushka.samples.heroes.models import CalendarTypes, CalendarMonthModel
from chatushka.samples.heroes.mongodb import get_calendar_collection


async def create_month() -> CalendarMonthModel:
    collection = get_calendar_collection()
    data = CalendarMonthModel()
    _: InsertOneResult = await collection.insert_one(data.dict())
    return data


async def get_current_month() -> CalendarMonthModel:
    collection = get_calendar_collection()
    now = datetime.now(tz=timezone.utc)
    doc = await collection.find_one(dict(type=CalendarTypes.MONTH))
    data = CalendarMonthModel(**doc) if doc else await create_month()
    if now.month != data.updated_at.month:
        data = await update_month()
    return data


async def update_month() -> CalendarMonthModel:
    collection = get_calendar_collection()
    data = CalendarMonthModel()
    res: UpdateResult = await collection.update_one(
        dict(type=CalendarTypes.MONTH),
        {
            "$set": dict(
                message=data.message,
            ),
            "$inc": dict(
                number=1,
            )
        },
    )
    if res:
        data.number += 1
    return data
