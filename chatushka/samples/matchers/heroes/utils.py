from random import choice, randrange
from typing import Optional

from chatushka.samples.matchers.heroes.messages import (
    PLAGUE_MONTH_MESSAGE,
    PLAYABLE_UNITS,
    REGULAR_MONTH_MESSAGE,
    REGULAR_MONTH_UNIT,
    REGULAR_WEEK_TEMPLATE,
    REGULAR_WEEK_UNIT,
    SPECIAL_MONTH_MESSAGE,
    SPECIAL_WEEK_TEMPLATE,
)

BOOL_TRUE_VALUES = ("+", "y", "yes", "true", "on")
BOOL_FALSE_VALUES = ("-", "n", "no", "false", "off")


def extract_state(
    args: list[str],
) -> Optional[bool]:
    if args and args[0] in BOOL_FALSE_VALUES:
        return False
    if args and args[0] in BOOL_TRUE_VALUES:
        return True
    return None


def _get_regular_week() -> str:
    beast = choice(REGULAR_WEEK_UNIT)
    return REGULAR_WEEK_TEMPLATE.format(beast=beast)


def _get_monster_week() -> str:
    unit = choice(PLAYABLE_UNITS)
    return SPECIAL_WEEK_TEMPLATE.format(beasts=unit)


def get_week_message() -> str:
    is_regular_week = randrange(4) != 0
    message = _get_regular_week() if is_regular_week else _get_monster_week()
    return message


def _get_regular_month() -> str:
    unit = choice(REGULAR_MONTH_UNIT)
    return REGULAR_MONTH_MESSAGE.format(unit=unit)


def _get_unit_month() -> str:
    unit = choice(REGULAR_MONTH_UNIT)
    return SPECIAL_MONTH_MESSAGE.format(unit=unit)


def get_month_message():
    random_int = randrange(10)
    if random_int < 5:
        return _get_regular_month()
    if random_int == 5:
        return PLAGUE_MONTH_MESSAGE
    return _get_unit_month()
