from typing import Iterable, Optional, Union, Dict, Set
from .typing import IGraph, T_VECTOR


class AdjacencyList(IGraph[T_VECTOR]):

    def adjacent(self, x: T_VECTOR, y: T_VECTOR) -> bool:
        if y not in self._verts:
            raise KeyError(y)
        return y in self._edges[x]

    def neighbors(self, x: T_VECTOR) -> Iterable[T_VECTOR]:
        return iter(self._edges[x])

    def add_vertex(self, x: T_VECTOR) -> None:
        if x in self:
            raise ValueError(x)
        self._ensure_vertex_exists(x)

    def remove_vertex(self, x: T_VECTOR) -> None:
        for y in list(self._edges[x]):
            self.remove_edge(x, y)
        for y, members in self._edges.items():
            if x in members:
                self.remove_edge(y, x)
        del self._verts[x]

    def add_edge(self, x: T_VECTOR, y: T_VECTOR) -> None:
        if y not in self._verts:
            raise KeyError(y)
        if y in self._edges[x]:
            raise ValueError(y)
        self._edges[x].add(y)

    def remove_edge(self, x: T_VECTOR, y: T_VECTOR) -> None:
        if x not in self._verts:
            raise KeyError(x)
        if y not in self._verts:
            raise KeyError(y)
        self._edges[x].remove(y)
        if (x, y) in self._weights:
            del self._weights[(x, y)]

    def get_weight(self, x: T_VECTOR, y: T_VECTOR) -> Optional[Union[int, float]]:
        if x not in self._verts:
            raise KeyError(x)
        if y not in self._verts:
            raise KeyError(y)
        return self._weights.get((x, y), None)

    def set_weight(self, x: T_VECTOR, y: T_VECTOR, w: Optional[Union[int, float]]) -> None:
        if x not in self._verts:
            raise KeyError(x)
        if y not in self._verts:
            raise KeyError(y)
        self._weights[(x, y)] = w

    def __getitem__(self, x: T_VECTOR) -> any:
        return self._verts[x]

    def __setitem__(self, x: T_VECTOR, v: any) -> None:
        self._ensure_vertex_exists(x)
        self._verts[x] = v

    def __contains__(self, x: T_VECTOR) -> bool:
        return x in self._verts

    def __iter__(self) -> Iterable[T_VECTOR]:
        return iter(self._verts.keys())

    def _ensure_vertex_exists(self, x: T_VECTOR) -> None:
        if x not in self:
            self._verts[x] = None
            self._edges[x] = set()

    def __init__(self):
        self._verts: Dict[T_VECTOR, any] = {}
        self._edges: Dict[T_VECTOR, Set[T_VECTOR]] = {}
        self._weights: Dict[Tuple[T_VECTOR, T_VECTOR], Union[int, float]] = {}

