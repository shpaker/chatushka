from typing import Optional, Union, Iterable, Hashable

from twowires.matchers.base import MatcherBase
from twowires.matchers.types import MatchedToken
from twowires.transports.models import Message


class CommandsMatcher(MatcherBase):

    suffix = "command"

    def __init__(
        self,
        prefixes: Union[str, tuple[str, ...]] = ("/",),
        postfixes: Union[str, tuple[str, ...]] = (),
        allow_raw: bool = False,
        case_sensitive: bool = False,
    ) -> None:

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

    async def _cast_token(
        self,
        token: Hashable,
    ) -> Union[Hashable, Iterable[Hashable]]:
        tokens = list()
        for variation in self._variations:
            value = variation.format(cmd=token)
            if self._case_sensitive:
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
            if self._case_sensitive:
                word = word.lower()
            if token == word:
                return MatchedToken(
                    token=token,
                    args=tuple(words[i+1:]),
                )
