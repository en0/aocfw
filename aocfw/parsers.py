from typing import Iterable, IO

from .typing import IParser


class IntegerParser(IParser):
    def parse(self, data: IO) -> Iterable[int]:
        return map(int, data)
