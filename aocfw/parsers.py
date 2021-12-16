from typing import Iterable, IO, Tuple

from .typing import IParser
from .adt.typing import IntVector2


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


class IntMapParser(IParser):
    def parse(self, data: IO) -> Iterable[Tuple[IntVector2, int]]:
        for y, line in enumerate(data):
            for x, c in enumerate(line.rstrip("\n")):
                yield IntVector2(x, y), int(c)
