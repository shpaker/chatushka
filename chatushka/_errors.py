from httpx import Response


class UshkoError(
    Exception,
):
    pass


class UshkoResponseError(
    UshkoError,
):
    def __init__(
        self,
        response: Response,
    ) -> None:
        super().__init__(f'Telegram response error: {response.text}"')
