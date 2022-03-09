from functools import lru_cache
from typing import Any, Dict

from yaml import safe_load

from chatushka.bot.settings import BOT_DATA_DIR


@lru_cache
def read_yaml_from_data_dir(
    filename: str,
) -> Dict[str, Any]:
    if not filename.endswith("yaml"):
        filename += ".yaml"
    path = BOT_DATA_DIR / filename
    with open(path, "r", encoding="utf8") as fh:
        data = fh.read()
    return safe_load(data)


def read_txt_from_data_dir(
    filename: str,
) -> list[str]:
    if not filename.endswith("txt"):
        filename += ".txt"
    path = BOT_DATA_DIR / filename
    with open(path, "r", encoding="utf8") as fh:
        data = fh.read()
    return data.strip().split("\n")
