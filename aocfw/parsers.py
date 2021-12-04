from typing import Iterable, IO

from .typing import IParser


class IntegerParser(IParser):
    def parse(self, data: IO) -> Iterable[int]:
        return map(int, data)


class StringParser(IParser):
    def parse(self, data: IO) -> Iterable[str]:
        return map(str, data)
