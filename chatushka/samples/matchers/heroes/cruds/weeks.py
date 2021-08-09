from datetime import datetime, timezone

from pymongo.results import InsertOneResult, UpdateResult

from chatushka.samples.matchers.heroes.models import CalendarTypes, CalendarWeekModel
from chatushka.samples.matchers.heroes.mongodb import get_calendar_collection


async def create_week() -> CalendarWeekModel:
    collection = get_calendar_collection()
    data = CalendarWeekModel()
    _: InsertOneResult = await collection.insert_one(data.dict())
    return data


async def get_current_week() -> CalendarWeekModel:
    collection = get_calendar_collection()
    now = datetime.now(tz=timezone.utc)
    _, week_now, _ = now.isocalendar()
    doc = await collection.find_one(dict(type=CalendarTypes.WEEK))
    data = CalendarWeekModel(**doc) if doc else await create_week()
    _, week_store, _ = data.updated_at.isocalendar()
    if week_now != week_store:
        data = await update_week()
    return data


async def update_week() -> CalendarWeekModel:
    collection = get_calendar_collection()
    data = CalendarWeekModel()
    res: UpdateResult = await collection.update_one(
        dict(type=CalendarTypes.WEEK),
        {
            "$set": dict(
                message=data.message,
            ),
            "$inc": dict(
                number=1,
            ),
        },
    )
    if res:
        data.number += 1
    return data
