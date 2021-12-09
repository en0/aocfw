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


class IConfiguration(ABC):

    @abstractmethod
    def new(self, path: str) -> None:
        ...

    @abstractmethod
    def get_session_token(self) -> str:
        ...

    @abstractmethod
    def set_session_token(self, value: str) -> None:
        ...

    @abstractmethod
    def get_year(self) -> int:
        ...

    @abstractmethod
    def set_year(self, value: int) -> None:
        ...


class IAOCClient(ABC):

    @abstractmethod
    def get_input(self, day: int, year: int) -> str:
        ...

    @abstractmethod
    def submit_answer(self, day: int, year: int, part: int, value: any) -> str:
        ...
