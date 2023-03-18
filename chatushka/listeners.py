import signal
from asyncio import ensure_future, get_event_loop, sleep
from functools import partial
from logging import getLogger

from chatushka import CommandsMatcher, EventsMatcher, EventTypes, Listener
from chatushka.__version__ import __URL__, __VERSION__
from chatushka.bot_api import TelegramBotAPI
from chatushka.constants import HTTP_POOLING_DELAY, HTTP_POOLING_TIMEOUT
from chatushka.models import Message
from chatushka.utils import check_preconditions

logger = getLogger(__name__)


async def _message_handler(
    bot_instance: Listener,
    message: Message,
    api: TelegramBotAPI,
) -> None:
    await api.send_message(
        chat_id=message.chat.id,
        text=bot_instance.help_message_text,
        reply_to_message_id=message.message_id,
        parse_mode="markdown",
        disable_web_page_preview=True,
    )


class Listener(EventsMatcher):
    def __init__(
        self,
        token: str,
        title: str = None,
        debug: bool = False,
    ) -> None:
        super().__init__()

        self.title = title or self.__class__.__name__
        self.debug = debug
        self.api = TelegramBotAPI(token)
        self.add_handler(EventTypes.STARTUP, check_preconditions, include_in_help=False)

        bot_commands_matcher = CommandsMatcher(prefixes=("!", "/"))
        bot_commands_matcher.add_handler(
            ("start", "help"),
            partial(_message_handler, self),
            help_message="This message!",
        )
        self.add_matcher(bot_commands_matcher)

    @property
    def help_message_text(self) -> str:
        output = f"*CHATUSHKA BOT {__VERSION__}*\n`/powered by {__URL__}/`"
        for help_message in self.help_messages:
            output += f"\n\n*{', '.join(help_message.tokens)}*\n> {help_message.message}"
        return output

    # pylint: disable=too-many-nested-blocks
    async def _loop(self) -> None:
        offset: int | None = None
        while True:
            try:
                updates, latest_update_id = await self.api.get_updates(
                    timeout=HTTP_POOLING_TIMEOUT,
                    offset=offset,
                )
                if updates:
                    offset = latest_update_id + 1
            except Exception as err:  # noqa, pylint: disable=broad-except
                logger.error(err)
                await sleep(HTTP_POOLING_DELAY)
                continue
            if updates:
                for update in updates:
                    try:
                        for matcher in self.matchers:
                            matched_handlers = await matcher.match(self.api, update, should_call_matched=True)
                            if matched_handlers:
                                logger.debug(f"Matched {len(matched_handlers)} handlers")
                    except Exception as err:  # noqa, pylint: disable=broad-except
                        if self.debug:
                            raise
                        logger.error(err)
            await sleep(HTTP_POOLING_DELAY)

    async def _close(self) -> None:
        await self.call(self.api, EventTypes.SHUTDOWN)
        for matcher in self.matchers:
            if isinstance(matcher, EventsMatcher):
                await matcher.call(api=self.api, token=EventTypes.SHUTDOWN)

    async def serve(self) -> None:
        await self.call(self.api, EventTypes.STARTUP)
        loop = get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, callback=lambda: ensure_future(self._close()))
            except NotImplementedError:
                break
        for matcher in self.matchers:
            await matcher.init()
            if isinstance(matcher, EventsMatcher):
                await matcher.call(api=self.api, token=EventTypes.STARTUP)
        await self._loop()