from typing import Hashable, Iterable, Optional, Union

from chatushka.matchers.base import MatcherBase
from chatushka.transports.models import Message
from chatushka.types import MatchedToken


class CommandsMatcher(MatcherBase):
    def __init__(
        self,
        prefixes: Union[str, tuple[str, ...]] = ("/",),
        postfixes: Union[str, tuple[str, ...]] = (),
        allow_raw: bool = False,
        case_sensitive: bool = False,
    ) -> None:

        super().__init__()
        if isinstance(prefixes, str):
            prefixes = (prefixes,)
        if isinstance(postfixes, str):
            prefixes = (prefixes,)

        variations = [prefix + "{cmd}" for prefix in prefixes if prefix.strip()] + [
            "{cmd}" + postfix for postfix in postfixes if postfix.strip()
        ]
        if allow_raw:
            variations.append("{cmd}")

        self._variations = set(variations)
        self._case_sensitive = case_sensitive

    def _cast_token(
        self,
        token: Hashable,
    ) -> Union[Hashable, Iterable[Hashable]]:
        tokens = list()
        for variation in self._variations:
            value = variation.format(cmd=token)
            if not self._case_sensitive:
                value = value.lower()
            tokens.append(value)
        return tokens

    async def _check(
        self,
        token: str,
        message: Message,
    ) -> Optional[MatchedToken]:
        words = tuple(word for word in message.text.split(" ") if word)
        for i, word in enumerate(words):
            if not self._case_sensitive:
                word = word.lower()
            if token == word:
                return MatchedToken(
                    token=token,
                    args=tuple(words[i + 1 :]),  # noqa
                )
