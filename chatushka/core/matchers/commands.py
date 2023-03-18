from collections.abc import Hashable, Iterable

from chatushka.core.matchers.base import MatcherBase
from chatushka.core.models import MatchedToken, Update


class CommandsMatcher(MatcherBase):
    def __init__(
        self,
        prefixes: str | tuple[str, ...] = ("/",),
        postfixes: str | tuple[str, ...] = (),
        allow_raw: bool = False,
        case_sensitive: bool = False,
        whitelist: tuple[int, ...] | None = None,
    ) -> None:
        super().__init__()
        if isinstance(prefixes, str):
            prefixes = (prefixes,)
        if isinstance(postfixes, str):
            postfixes = (postfixes,)

        variations = [prefix + "{cmd}" for prefix in prefixes if prefix.strip()] + [
            "{cmd}" + postfix for postfix in postfixes if postfix.strip()
        ]
        if allow_raw:
            variations.append("{cmd}")

        self._variations = set(variations)
        self._case_sensitive = case_sensitive
        self._whitelist = whitelist

    def _cast_token(
        self,
        token: Hashable,
    ) -> Hashable | Iterable[Hashable]:
        tokens = []
        for variation in self._variations:
            value = variation.format(cmd=token)
            if not self._case_sensitive:
                value = value.lower()
            tokens.append(value)
        return tokens

    async def _check(
        self,
        token: str,
        update: Update,
    ) -> MatchedToken | None:
        if not update.message or not update.message.text:
            return None
        if self._whitelist and update.message.user.id not in self._whitelist:
            return None
        words = tuple(word for word in update.message.text.split(" ") if word)
        for i, word in enumerate(words):
            if not self._case_sensitive:
                word = word.lower()
            if token == word:
                return MatchedToken(
                    token=token,
                    args=tuple(words[i + 1 :]),
                )
        return None
