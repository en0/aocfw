from abc import abstractmethod
from typing import Generic, TypeVar, Hashable, Iterable, Optional, Union


T_VECTOR = TypeVar("T_VECTOR", bound=Hashable)


class IGraph(Generic[T_VECTOR]):
    """Unweighted Graph Interface"""

    @abstractmethod
    def adjacent(self, x: T_VECTOR, y: T_VECTOR) -> bool:
        """Tests whether there is an edge from the vertex x to the vertex y.

        Raises:
          KeyError:
            - If x is not a member of the graph.
            - If y is not a member of the graph.
        """
        ...

    @abstractmethod
    def neighbors(self, x: T_VECTOR) -> Iterable[T_VECTOR]:
        """List all vertices y such that there is an edge from the vertex x to the vertex y

        Raises:
          KeyError: if x is not a member of the graph.
        """
        ...

    @abstractmethod
    def add_vertex(self, x: T_VECTOR) -> None:
        """Add the vertex x.

        Raises:
          ValueError: if x is already a member.
        """
        ...

    @abstractmethod
    def remove_vertex(self, x: T_VECTOR) -> None:
        """Removes the vertex x

        Raises:
          KeyError: If x is not a member of the graph.
        """
        ...

    @abstractmethod
    def add_edge(self, x: T_VECTOR, y: T_VECTOR) -> None:
        """Adds the edge from the vertex x to the vertex y

        Raises:
          ValueError if an edge already exists between vertex x and vertex y.
          KeyError:
            - If x is not a member of the graph.
            - If y is not a member of the graph.
        """
        ...

    @abstractmethod
    def remove_edge(self, x: T_VECTOR, y: T_VECTOR) -> None:
        """Removes the edge from the vertex x to the vertex y.

        Raises:
          KeyError:
            - If x is not a member of the graph.
            - If y is not a member of the graph.
            - If there is no edge between x and y.
        """
        ...

    @abstractmethod
    def get_weight(self, x: T_VECTOR, y: T_VECTOR) -> Optional[Union[int, float]]:
        """Returns the weight of the edge between the vector x and the vector y.

        Raises:
          KeyError:
            - If x is not a member of the graph.
            - If y is not a member of the graph.
        """
        ...

    @abstractmethod
    def set_weight(self, x: T_VECTOR, y: T_VECTOR, w: Optional[Union[int, float]]) -> None:
        """Sets the value associated with the edge between the vector x and the vector y.

        Raises:
          KeyError:
            - If x is not a member of the graph.
            - If y is not a member of the graph.
        """
        ...

    @abstractmethod
    def __getitem__(self, x: T_VECTOR) -> any:
        """Returns the value associated with the vertex x.

        Raises:
          KeyError: If x is not a member of the graph.
        """
        ...

    @abstractmethod
    def __setitem__(self, x: T_VECTOR, v: any) -> None:
        """Sets the value associated with the vertex x to the value v

        If the vertex x does not exist, it will be created.
        """
        ...

    @abstractmethod
    def __contains__(self, x: T_VECTOR) -> bool:
        """Tests whether the vertex x exists in the graph or not."""
        ...

    @abstractmethod
    def __iter__(self) -> Iterable[T_VECTOR]:
        """Returns an iterator of vertices contained in the graph"""
        ...
