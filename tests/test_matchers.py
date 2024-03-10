from typing import Type

from pytest import mark, param, raises

from chatushka._matchers import CommandMatcher, RegexMatcher
from chatushka._matchers import HandlersContainer
from chatushka._models import Message, User, Chat, ChatType
from chatushka._models import Update
from chatushka._transport import TelegramBotAPI


def _make_update(
    text: str,
) -> Update:
    return Update(
        update_id=780080167,
        message=Message(
            message_id=164380,
            user=User(
                id=777000,
                is_bot=False,
                first_name="Telegram",
                last_name=None,
                can_join_groups=None,
                can_read_all_group_messages=None,
            ),
            chat=Chat(
                id=-1001357425012,
                type=ChatType.SUPERGROUP,
                title="биг блк дик",
            ),
            text=text,
            reply_to_message=None,
            new_chat_members=[],
        ),
        my_chat_member=None,
    )


async def test_call_handler_async_func() -> None:
    async def _func() -> None:
        raise RuntimeError

    with raises(
        RuntimeError,
    ):
        await HandlersContainer._call_handler(
            handler=_func,
            api=TelegramBotAPI(token="token"),
            update=Update(
                update_id="911",
            ),
        )


async def test_call_handler_sync_func() -> None:
    async def _func() -> None:
        raise RuntimeError

    with raises(
        RuntimeError,
    ):
        await HandlersContainer._call_handler(
            handler=_func,
            api=TelegramBotAPI(token="token"),
            update=Update(
                update_id="911",
            ),
        )


async def test_call_handler_with_param() -> None:
    def _func(
        err_type: Type[Exception],
    ) -> None:
        raise err_type

    with raises(
        ValueError,
    ):
        await HandlersContainer._call_handler(
            handler=_func,
            api=TelegramBotAPI(token="token"),
            update=Update(
                update_id="911",
            ),
            err_type=ValueError,
        )


@mark.parametrize(
    "token, prefixes, case_sensitive, text",
    [
        param("test", "", False, "test bar", id="ok"),
        param("test", "", True, "tESt bar", id="not case_sensitive"),
        param("test", "!", True, "!test bar", id="with prefix"),
        param("test", ["!", "?"], True, "?test bar", id="several prefixes"),
    ],
)
async def test_command_matcher_success(
    token: str,
    prefixes: str | list[str],
    case_sensitive: bool,
    text: str,
) -> None:
    matcher = CommandMatcher(
        prefixes=prefixes,
        case_sensitive=case_sensitive,
    )

    @matcher(token)
    def _handler() -> None:
        raise RuntimeError

    results = await matcher.check_handlers(
        api=TelegramBotAPI(token="123:abc"),
        update=_make_update(text),
    )
    assert len(results) == 1, len(results)
    with raises(RuntimeError):
        await results[0]


@mark.parametrize(
    "token, prefix, case_sensitive, text",
    [
        ("test", "", False, "foo bar"),
        ("test", "", False, "foo TEST bar"),
        ("test", "!", True, "foo test bar"),
    ],
)
async def test_command_matcher_fail(
    token: str,
    prefix: str,
    case_sensitive: bool,
    text: str,
) -> None:
    matcher = CommandMatcher(
        prefixes=prefix,
        case_sensitive=case_sensitive,
    )

    @matcher(token)
    def _handler() -> None:
        raise RuntimeError

    results = await matcher.check_handlers(
        api=TelegramBotAPI(token="123:abc"),
        update=_make_update(text),
    )
    assert len(results) == 0, len(results)


async def test_regex_matcher_success() -> None:
    matcher = RegexMatcher()

    @matcher("^a...s$")
    def _handler() -> None:
        raise RuntimeError

    results = await matcher.check_handlers(
        api=TelegramBotAPI(token="123:abc"),
        update=_make_update("abyss"),
    )
    assert len(results) == 1, len(results)
    with raises(RuntimeError):
        await results[0]


async def test_regex_matcher_fail() -> None:
    matcher = RegexMatcher()

    @matcher("^a...s$")
    def _handler() -> None:
        raise RuntimeError

    results = await matcher.check_handlers(
        api=TelegramBotAPI(token="123:abc"),
        update=_make_update("11abyss"),
    )
    assert len(results) == 0, len(results)
