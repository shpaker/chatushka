from chatushka.utils import ServiceSettingsBase


class MongoDBSettings(ServiceSettingsBase):
    mongodb_dsn: str
    mongodb_min_connections_count: int = 2
    mongodb_max_connections_count: int = 8
