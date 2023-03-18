from click import command, option

from chatushka.bot.cli_main import cli_main


@command()
@option(
    "--token",
    "-t",
    required=True,
)
@option(
    "--debug/--no-debug",
    is_flag=True,
)
def main(
    token: str,
    debug: bool,
) -> None:
    cli_main(token=token, debug=debug)
