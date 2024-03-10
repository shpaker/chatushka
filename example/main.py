from asyncio import run

from click import command, option, types

from chatushka import ChatushkaBot


def make_bot(
    token: str,
) -> ChatushkaBot:
    bot = ChatushkaBot(
        token=token,
    )
    return bot


@command()
@option(
    "--token",
    "-t",
    required=True,
)
@option(
    "--sentry-dsn",
    required=False,
)
def cli_main(
    token: str,
    sentry_dsn: str | None,
) -> None:
    bot = make_bot(token)
    run(bot.start())
