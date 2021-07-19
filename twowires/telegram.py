from logging import getLogger
from typing import Any, Dict, List, Optional, Tuple, Union

from httpx import AsyncClient, Response
from pydantic import ValidationError

from twowires.models import telegram_types
from twowires.models.telegram_types import ChatType
from twowires.settings import get_settings

ALLOWED_CHAT_TYPES_FOR_UPDATES = (
    ChatType.GROUP,
    ChatType.SUPERGROUP,
)

logger = getLogger()
settings = get_settings()


def _base_api_url() -> str:
    return f"https://api.telegram.org/bot{settings.token}"


def _api_method_url(
    method: str,
) -> str:
    return f"{_base_api_url()}/{method}"


def check_telegram_response(
    response: Response,
) -> Dict[str, Any]:
    data: dict[str, Any] = response.json()
    is_ok: bool = data.get("ok", False)
    if not is_ok:
        raise ValueError(f"Telegram response error: {response.text}")
    result: Dict[str, Any] = data["result"]
    return result


async def _call_api(
    method: str,
    timeout: int = 10,
    **kwargs: Any,
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    url = _api_method_url(method)
    async with AsyncClient() as client:  # type: AsyncClient
        response = await client.post(url, timeout=timeout * 2, data=kwargs)
    response.raise_for_status()
    return check_telegram_response(response)


async def get_me() -> telegram_types.User:
    result = await _call_api("getme")
    return telegram_types.User(**result)  # type: ignore


async def get_updates(timeout: int, offset: Optional[int] = None) -> Tuple[List[telegram_types.Update], int]:
    params = dict()
    if offset:
        params["offset"] = offset
    results = await _call_api(
        "getupdates",
        timeout=timeout,
        **params,
    )
    updates_list = list()
    latest_update_id: Optional[int] = offset
    for result in results:
        if not latest_update_id or (latest_update_id < result["update_id"]):  # type: ignore
            latest_update_id = result["update_id"]  # type: ignore
        try:
            update = telegram_types.Update(**result)  # type: ignore
        except ValidationError:
            continue
        updates_list.append(update)
    return updates_list, latest_update_id  # type: ignore


async def send_message(
    chat_id: int,
    text: str,
    reply_to_message_id: int,
) -> telegram_types.Message:
    result = await _call_api(
        "sendmessage",
        chat_id=chat_id,
        text=text,
        reply_to_message_id=reply_to_message_id,
        parse_mode="html",
        disable_web_page_preview=True,
    )
    return telegram_types.Message(**result)  # type: ignore
