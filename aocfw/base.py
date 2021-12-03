from abc import abstractmethod
from typing import Iterable, Dict, Type, TypeVar
from pyioc3 import StaticContainerBuilder, Container

from .loaders import FileLoader
from .parsers import IntegerParser
from .typing import IParser, ILoader, ISolution


TYPE_T = TypeVar("TYPE_T")


class SolutionBase(ISolution):

    _ioc: Container = None
    _bindings = {
        ILoader: FileLoader,
        IParser: IntegerParser,
    }

    bindings: Dict[Type, Type] = {}

    @abstractmethod
    def solve(self, data: Iterable[any]) -> any:
        ...

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
    def run(cls, **kwargs):

        bindings = cls._bindings.copy()
        bindings.update(cls.bindings)

        ioc_builder = StaticContainerBuilder()
        for a, i in bindings.items():
            ioc_builder.bind(a, i)
        ioc_builder.bind(cls, cls)

        cls._ioc = ioc_builder.build()
        solution = cls.get(cls)
        ans = solution._solve(**kwargs)
        print(f"Answer: {ans}")
