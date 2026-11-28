"""Generic undirected graph container backed by an adjacency list."""

from __future__ import annotations

from copy import deepcopy
from functools import total_ordering
from typing import Dict, Generic, List, Tuple, TypeVar

from lab4.constants import EMPTY_GRAPH_LABEL
from lab4.exceptions import (
    ConstIteratorError,
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    InvalidIteratorError,
    SelfLoopNotAllowedError,
    VertexAlreadyExistsError,
    VertexNotFoundError,
)
from lab4.graph.iterators import BidirectionalIterator

VertexValue = TypeVar("VertexValue")
EdgeTuple = Tuple[VertexValue, VertexValue]


@total_ordering
class UndirectedGraph(Generic[VertexValue]):
    """Generic undirected graph implemented via an encapsulated adjacency list."""

    def __init__(self) -> None:
        """Initialize an empty undirected graph."""
        # Внутренний список смежности: вершина -> список смежных вершин
        self._adjacency_list: Dict[VertexValue, List[VertexValue]] = {}

    def copy(self) -> UndirectedGraph[VertexValue]:
        """Return a deep copy of the graph."""
        cloned_graph: UndirectedGraph[VertexValue] = UndirectedGraph()
        cloned_graph._adjacency_list = deepcopy(self._adjacency_list)
        return cloned_graph

    def assign_from(self, other: UndirectedGraph[VertexValue]) -> None:
        """Replace current graph contents with a deep copy of another graph."""
        if not isinstance(other, UndirectedGraph):
            raise TypeError("Expected an UndirectedGraph instance.")
        self._adjacency_list = deepcopy(other._adjacency_list)

    def is_empty(self) -> bool:
        """Return True if the graph contains no vertices."""
        return len(self._adjacency_list) == 0

    def clear(self) -> None:
        """Remove all vertices and edges from the graph."""
        self._adjacency_list.clear()

    def has_vertex(self, vertex: VertexValue) -> bool:
        """Return True if the vertex exists in the graph."""
        return vertex in self._adjacency_list

    def has_edge(self, first_vertex: VertexValue, second_vertex: VertexValue) -> bool:
        """Return True if an undirected edge connects the two vertices."""
        if not self.has_vertex(first_vertex) or not self.has_vertex(second_vertex):
            return False
        return second_vertex in self._adjacency_list[first_vertex]

    def vertex_count(self) -> int:
        """Return the total number of vertices in the graph."""
        return len(self._adjacency_list)

    def edge_count(self) -> int:
        """Return the total number of undirected edges in the graph."""
        # Сумма степеней всех вершин равна удвоенному количеству рёбер
        total_degrees = sum(len(neighbors) for neighbors in self._adjacency_list.values())
        return total_degrees // 2

    def vertex_degree(self, vertex: VertexValue) -> int:
        """Return the degree (number of incident edges) of the given vertex."""
        self._require_vertex(vertex)
        return len(self._adjacency_list[vertex])

    def edge_degree(self, first_vertex: VertexValue, second_vertex: VertexValue) -> int:
        """Return the degree of an edge (count of adjacent edges)."""
        if not self.has_edge(first_vertex, second_vertex):
            raise EdgeNotFoundError(
                f"Edge ({first_vertex!r}, {second_vertex!r}) does not exist."
            )
        # Степень ребра — сумма степеней его концов без учёта самого ребра (минус 2)
        first_degree = len(self._adjacency_list[first_vertex])
        second_degree = len(self._adjacency_list[second_vertex])
        return first_degree + second_degree - 2

    def add_vertex(self, vertex: VertexValue) -> None:
        """Add a new vertex to the graph."""
        if self.has_vertex(vertex):
            raise VertexAlreadyExistsError(f"Vertex {vertex!r} already exists.")
        self._adjacency_list[vertex] = []

    def add_edge(self, first_vertex: VertexValue, second_vertex: VertexValue) -> None:
        """Add an undirected edge between two existing vertices."""
        self._require_vertex(first_vertex)
        self._require_vertex(second_vertex)
        if first_vertex == second_vertex:
            raise SelfLoopNotAllowedError("Self-loops are not allowed in a simple graph.")
        if self.has_edge(first_vertex, second_vertex):
            raise EdgeAlreadyExistsError(
                f"Edge ({first_vertex!r}, {second_vertex!r}) already exists."
            )

        self._adjacency_list[first_vertex].append(second_vertex)
        self._adjacency_list[second_vertex].append(first_vertex)

    def remove_vertex(self, vertex: VertexValue) -> None:
        """Remove a vertex and all edges incident to it."""
        self._require_vertex(vertex)
        # Удаляем упоминания вершины из списков смежности всех её соседей
        neighbors = list(self._adjacency_list[vertex])
        for neighbor in neighbors:
            self._adjacency_list[neighbor].remove(vertex)
        del self._adjacency_list[vertex]

    def remove_edge(self, first_vertex: VertexValue, second_vertex: VertexValue) -> None:
        """Remove an existing undirected edge between two vertices."""
        if not self.has_edge(first_vertex, second_vertex):
            raise EdgeNotFoundError(
                f"Edge ({first_vertex!r}, {second_vertex!r}) does not exist."
            )
        self._adjacency_list[first_vertex].remove(second_vertex)
        self._adjacency_list[second_vertex].remove(first_vertex)

    def remove_vertex_by_iterator(
        self,
        iterator: BidirectionalIterator[VertexValue],
    ) -> None:
        """Remove the vertex currently pointed to by a mutable vertex iterator."""
        self._validate_mutable_iterator(iterator)
        target_vertex = iterator.current()
        self.remove_vertex(target_vertex)

    def remove_edge_by_iterator(
        self,
        iterator: BidirectionalIterator[EdgeTuple[VertexValue]],
    ) -> None:
        """Remove the edge currently pointed to by a mutable edge iterator."""
        self._validate_mutable_iterator(iterator)
        first_vertex, second_vertex = iterator.current()
        self.remove_edge(first_vertex, second_vertex)

    def vertices_iter(
        self,
        *,
        reverse: bool = False,
        const: bool = False,
    ) -> BidirectionalIterator[VertexValue]:
        """Return a bidirectional iterator over all vertices."""
        vertices = list(self._adjacency_list.keys())
        return BidirectionalIterator(
            vertices,
            is_reverse=reverse,
            is_const=const,
            owner_id=id(self),
        )

    def edges_iter(
        self,
        *,
        reverse: bool = False,
        const: bool = False,
    ) -> BidirectionalIterator[EdgeTuple[VertexValue]]:
        """Return a bidirectional iterator over all unique undirected edges."""
        edges = self._collect_unique_edges()
        return BidirectionalIterator(
            edges,
            is_reverse=reverse,
            is_const=const,
            owner_id=id(self),
        )

    def incident_edges_iter(
        self,
        vertex: VertexValue,
        *,
        reverse: bool = False,
        const: bool = False,
    ) -> BidirectionalIterator[EdgeTuple[VertexValue]]:
        """Return a bidirectional iterator over edges incident to a vertex."""
        self._require_vertex(vertex)
        incident_edges = [(vertex, neighbor) for neighbor in self._adjacency_list[vertex]]
        return BidirectionalIterator(
            incident_edges,
            is_reverse=reverse,
            is_const=const,
            owner_id=id(self),
        )

    def adjacent_vertices_iter(
        self,
        vertex: VertexValue,
        *,
        reverse: bool = False,
        const: bool = False,
    ) -> BidirectionalIterator[VertexValue]:
        """Return a bidirectional iterator over vertices adjacent to a vertex."""
        self._require_vertex(vertex)
        neighbors = list(self._adjacency_list[vertex])
        return BidirectionalIterator(
            neighbors,
            is_reverse=reverse,
            is_const=const,
            owner_id=id(self),
        )

    def __eq__(self, other: object) -> bool:
        """Compare two graphs for structural equality (same vertices and edges)."""
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        return self._canonical_state() == other._canonical_state()

    def __lt__(self, other: object) -> bool:
        """Compare two graphs by vertex count, edge count, and canonical state."""
        if not isinstance(other, UndirectedGraph):
            return NotImplemented
        left_key = (self.vertex_count(), self.edge_count(), self._canonical_state())
        right_key = (other.vertex_count(), other.edge_count(), other._canonical_state())
        return left_key < right_key

    def __str__(self) -> str:
        """Build a string representation of the graph using its iterators."""
        if self.is_empty():
            return EMPTY_GRAPH_LABEL

        # Формируем текстовое представление строго через константные итераторы графа
        vertices_text = ", ".join(repr(vertex) for vertex in self.vertices_iter(const=True))
        edges_text = ", ".join(
            f"({first!r} -- {second!r})"
            for first, second in self.edges_iter(const=True)
        )
        return f"UndirectedGraph(vertices=[{vertices_text}], edges=[{edges_text}])"

    def _require_vertex(self, vertex: VertexValue) -> None:
        """Raise VertexNotFoundError if the vertex is missing."""
        if not self.has_vertex(vertex):
            raise VertexNotFoundError(f"Vertex {vertex!r} does not exist.")

    def _validate_mutable_iterator(self, iterator: BidirectionalIterator) -> None:
        """Verify that an iterator belongs to this graph and is not read-only."""
        if iterator.owner_id != id(self):
            raise InvalidIteratorError("Iterator does not belong to this graph.")
        if iterator.is_const:
            raise ConstIteratorError("Cannot modify graph using a read-only iterator.")

    def _collect_unique_edges(self) -> List[EdgeTuple[VertexValue]]:
        """Collect all unique undirected edges without duplicating (u, v) and (v, u)."""
        seen_vertices: List[VertexValue] = []
        unique_edges: List[EdgeTuple[VertexValue]] = []

        for vertex, neighbors in self._adjacency_list.items():
            for neighbor in neighbors:
                if neighbor not in seen_vertices:
                    unique_edges.append((vertex, neighbor))
            seen_vertices.append(vertex)

        return unique_edges

    def _canonical_state(self) -> Tuple[Tuple[str, ...], Tuple[Tuple[str, str], ...]]:
        """Return a deterministic, order-independent representation for comparisons."""
        sorted_vertices = tuple(sorted(repr(vertex) for vertex in self._adjacency_list))
        normalized_edges = [
            tuple(sorted((repr(first), repr(second))))
            for first, second in self._collect_unique_edges()
        ]
        sorted_edges = tuple(sorted(normalized_edges))
        return sorted_vertices, sorted_edges
