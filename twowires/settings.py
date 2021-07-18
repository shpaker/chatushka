from functools import lru_cache
from os import mkdir
from os.path import exists
from pathlib import Path
from typing import Any, Dict

from pydantic import validator, BaseSettings, DirectoryPath, FilePath

SETTINGS_ENV_PREFIX = "bot_"


class _Settings(BaseSettings):
    token: str
    debug: bool = False
    data_dir: DirectoryPath = Path.home() / f'.twowires'
    update_data_file: FilePath = "updates.json"

    @validator("data_dir", always=True, pre=True)
    def check_data_dir(
        cls,
        value: str,
    ) -> Path:
        value = Path(value).resolve()
        if not exists(value):
            mkdir(value)
        return value

    @validator("update_data_file", always=True, pre=True)
    def check_update_data_file(
        cls,
        value: str,
        values: Dict[str, Any],
        **kwargs,  # noqa
    ) -> Path:
        data_dir: Path = values["data_dir"]
        value = data_dir.resolve() / value
        if not exists(value):
            with open(value, "a") as file:
                file.close()
        return value

    class Config:
        env_prefix = SETTINGS_ENV_PREFIX
        env_file = ".env"
        allow_mutation = False


@lru_cache
def get_settings():
    return _Settings()
