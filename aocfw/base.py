from abc import abstractmethod
from typing import Iterable, Dict, Type, TypeVar, IO
from pyioc3 import StaticContainerBuilder, Container

from .loaders import AutoLoader
from .parsers import IntegerParser
from .typing import IParser, ILoader, ISolution


TYPE_T = TypeVar("TYPE_T")


class SolutionBase(ISolution):

    _ioc: Container = None
    _bindings = {
        ILoader: AutoLoader,
        IParser: IntegerParser,
    }

    bindings: Dict[Type, Type] = {}

    @abstractmethod
    def solve(self, data: Iterable[any]) -> any:
        ...

    def _load_and_parse(self, **kwargs) -> Iterable[any]:
        def callback(data):
            parser = self.get(IParser)
            data = parser.parse(data)
            return iter(list(data))
        loader = self.get(ILoader)
        ans = loader.read(callback=callback, **kwargs)
        return ans

    def _solve(self, **kwargs) -> any:
        def callback(data):
            parser = self.get(IParser)
            _data = parser.parse(data)
            return self.solve(_data)
        loader = self.get(ILoader)
        ans = loader.read(callback=callback, **kwargs)
        return ans

    @classmethod
    def get(cls, annotation: Type[TYPE_T]) -> TYPE_T:
        return cls._ioc.get(annotation)

    @classmethod
    def run(cls, **kwargs) -> None:
        ans = cls.check(**kwargs)
        print(f"Answer: {ans}")

    @classmethod
    def check(cls, **kwargs) -> any:
        cls._bind()
        return cls.get(cls)._solve(**kwargs)

    @classmethod
    def parse(cls, **kwargs):
        cls._bind()
        return cls.get(cls)._load_and_parse(**kwargs)

    @classmethod
    def new(cls, **kwargs):
        cls._bind()
        return cls.get(cls)

    @classmethod
    def _bind(cls):
        bindings = cls._bindings.copy()
        bindings.update(cls.bindings)
        ioc_builder = StaticContainerBuilder()
        for a, i in bindings.items():
            ioc_builder.bind(a, i)
        ioc_builder.bind(cls, cls)
        cls._ioc = ioc_builder.build()
