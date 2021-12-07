from typing import Iterable, IO

from .typing import IParser


class IntegerParser(IParser):
    def parse(self, data: IO) -> Iterable[int]:
        return map(int, data)


class OneLineIntegerParser(IParser):
    def parse(self, data: IO) -> Iterable[any]:
        data = map(lambda x: str(x).rstrip("\n"), data)
        return map(int, ",".join(data).split(","))


class StringParser(IParser):
    def parse(self, data: IO) -> Iterable[str]:
        return map(lambda x: str(x).rstrip("\n"), data)

