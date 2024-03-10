from types import TracebackType
from typing import Any, Literal

from httpx import AsyncClient, Response

from chatushka._constants import HTTP_REGULAR_TIMEOUT
from chatushka._errors import UshkoResponseError
from chatushka._models import (
    ChatMemberAdministrator,
    ChatMemberOwner,
    ChatMemberStatuses,
    Message,
    Update,
)


async def _raise_on_api_error_response_event_hook(
    response: Response,
) -> None:
    response.raise_for_status()
    await response.aread()
    data: dict[str, Any] = response.json()
    if data.get("ok", False) is False or data.get("result") is None:
        raise UshkoResponseError(
            response=response,
        )


class TelegramBotAPI:
    def __init__(
        self,
        token: str,
        timeout: int = HTTP_REGULAR_TIMEOUT,
    ) -> None:
        self._latest_update_id: int | None = None
        self._client = AsyncClient(
            base_url=f"https://api.telegram.org/bot{token}",
            event_hooks={  # type: ignore
                "response": [
                    _raise_on_api_error_response_event_hook,
                ]
            },
            timeout=timeout,
        )
        self._timeout = timeout

    async def _api_request(
        self,
        api_method: str,
        **kwargs: Any,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        response = await self._client.post(
            url=api_method,
            data=kwargs,
        )
        return response.json()["result"]

    async def __aenter__(
        self,
    ) -> "TelegramBotAPI":
        await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        return await self._client.__aexit__(
            exc_type=exc_type,
            exc_value=exc_value,
            traceback=traceback,
        )

    async def get_updates(
        self,
    ) -> list[Update]:
        offset: int | None = None
        if self._latest_update_id is not None:
            offset = self._latest_update_id + 1
        params = {} if not offset else {"offset": offset}
        if self._timeout:
            params["timeout"] = self._timeout
        results = [
            Update.model_validate(entry)
            for entry in await self._api_request(
                api_method="getUpdates",
                **params,
            )
        ]
        self._latest_update_id = results[-1].update_id
        return results

    async def send_message(
        self,
        chat_id: int,
        text: str,
        reply_to_message_id: int | None = None,
        parse_mode: Literal["html", "markdown"] = "html",
        disable_web_page_preview: bool = False,
    ) -> Message:
        result = await self._api_request(
            api_method="sendMessage",
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
        )
        return Message.model_validate(result)

    async def get_chat_administrators(
        self,
        chat_id: int,
    ) -> list[ChatMemberAdministrator | ChatMemberOwner]:
        results = await self._api_request(
            "getChatAdministrators",
            chat_id=chat_id,
        )
        admins: list[ChatMemberAdministrator | ChatMemberOwner] = []
        for result in results:
            status = result["status"]  # type: ignore
            if status == ChatMemberStatuses.CREATOR:
                admins.append(ChatMemberOwner.model_validate(result))
            if status == ChatMemberStatuses.ADMINISTRATOR:
                admins.append(ChatMemberAdministrator.model_validate(result))
        return admins