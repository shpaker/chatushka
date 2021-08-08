from logging import getLogger

from motor.motor_asyncio import AsyncIOMotorClient

from chatushka.services.base import ServiceWrapperBase
from chatushka.services.mongodb.settings import MongoDBSettings

logger = getLogger(__name__)


class MongoDBWrapper(ServiceWrapperBase):
    def __init__(self) -> None:
        super().__init__()
        self.healthz_name = "mongodb"
        self.client: AsyncIOMotorClient
        self.settings: MongoDBSettings = MongoDBSettings()

    async def startup_event_handler(
        self,
    ) -> None:
        self.client = AsyncIOMotorClient(  # noqa
            self.settings.mongodb_dsn,
            minPoolSize=self.settings.mongodb_min_connections_count,
            maxPoolSize=self.settings.mongodb_max_connections_count,
            uuidRepresentation="standard",
        )

    async def shutdown_event_handler(self) -> None:
        if self.client:
            self.client.close()

    async def health_check(self) -> None:
        await self.client.conn.command({"dbStats": 1})
