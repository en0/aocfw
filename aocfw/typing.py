from abc import abstractmethod, ABC
from typing import Iterable, IO, Callable


class IParser(ABC):
    @abstractmethod
    def parse(self, data: IO) -> Iterable[any]:
        ...


class ILoader(ABC):
    @abstractmethod
    def read(self, callback: Callable[[IO], any], **kwargs) -> any:
        ...


class ISolution(ABC):
    @abstractmethod
    def solve(self, data: Iterable[any]) -> any:
        ...
