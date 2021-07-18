from asyncio import iscoroutinefunction, sleep
from datetime import datetime, timedelta
from typing import Callable, Coroutine, Union, Optional
from logging import getLogger
from twowires.telegram import get_updates
from twowires.tokens import check_tokens

UPDATE_DELAY = timedelta(seconds=2)

logger = getLogger(__name__)


class TwoWiresBot:

    _event_handlers: dict[
        str,
        list[Union[Callable[[], None], Callable[[], Coroutine]]]
    ] = dict()

    def add_event_handler(
        self,
        event: str,
        handler: Union[Callable[[], None], Callable[[], Coroutine]],
    ):
        if event not in self._event_handlers:
            self._event_handlers[event] = list()
        self._event_handlers[event].append(handler)

    async def loop(self):
        offset: Optional[int] = None
        next_update: Optional[datetime] = datetime.now()
        while True:
            current_ts = datetime.now()
            if current_ts >= next_update:
                updates, latest_update_id = await get_updates(offset=offset)
                if updates:
                    logger.info(f"Receive {len(updates)} messages, next offset from {offset}")
                    for update in updates:
                        logger.debug(f" + [{update.update_id}]"
                                     f" {update.message.chat.title}"
                                     f" > {update.message.user.readable_name}"
                                     f" > {update.message.text}")
                    offset = latest_update_id + 1
                await check_tokens(updates)
                next_update = current_ts + UPDATE_DELAY
            await sleep(1)

    async def serve(self):
        for handler in (_ := self._event_handlers.get("startup", list())):
            if iscoroutinefunction(handler):
                await handler()
                continue
            handler()
        await self.loop()

