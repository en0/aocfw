from abc import ABC, abstractmethod
from argparse import _SubParsersAction, ArgumentParser
from typing import Optional


class IEntryPoint(ABC):

    @staticmethod
    @abstractmethod
    def argdef(sp: _SubParsersAction) -> ArgumentParser:
        raise NotImplementedError()

    @abstractmethod
    def run(self) -> Optional[int]:
        raise NotImplementedError()
