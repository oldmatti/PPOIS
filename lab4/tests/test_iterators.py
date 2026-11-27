"""Unit tests for bidirectional, reverse, and const graph iterators."""

import unittest

from lab4.exceptions import (
    ConstIteratorError,
    InvalidIteratorError,
    VertexNotFoundError,
)
from lab4.graph import UndirectedGraph


class TestGraphIterators(unittest.TestCase):
    """Tests for all iterator types and iterator-based removal."""

    def setUp(self) -> None:
        """Create a connected graph for iterator tests."""
        self.graph: UndirectedGraph[str] = UndirectedGraph()
        for vertex in ("A", "B", "C"):
            self.graph.add_vertex(vertex)
        self.graph.add_edge("A", "B")
        self.graph.add_edge("A", "C")
        self.graph.add_edge("B", "C")

    def test_vertices_and_edges_iterators_forward_and_reverse(self) -> None:
        """Verify forward and reverse iteration over vertices and edges."""
        forward_vertices = list(self.graph.vertices_iter())
        reverse_vertices = list(self.graph.vertices_iter(reverse=True))
        self.assertEqual(forward_vertices, ["A", "B", "C"])
        self.assertEqual(reverse_vertices, ["C", "B", "A"])

        forward_edges = list(self.graph.edges_iter())
        reverse_edges = list(self.graph.edges_iter(reverse=True))
        self.assertEqual(len(forward_edges), 3)
        self.assertEqual(reverse_edges, list(reversed(forward_edges)))

    def test_incident_edges_and_adjacent_vertices_iterators(self) -> None:
        """Verify incident edges and adjacent vertices iterators."""
        neighbors = list(self.graph.adjacent_vertices_iter("A"))
        rev_neighbors = list(self.graph.adjacent_vertices_iter("A", reverse=True))
        self.assertEqual(neighbors, ["B", "C"])
        self.assertEqual(rev_neighbors, ["C", "B"])

        incident = list(self.graph.incident_edges_iter("A"))
        rev_incident = list(self.graph.incident_edges_iter("A", reverse=True))
        self.assertEqual(incident, [("A", "B"), ("A", "C")])
        self.assertEqual(rev_incident, [("A", "C"), ("A", "B")])

        with self.assertRaises(VertexNotFoundError):
            self.graph.adjacent_vertices_iter("Z")
        with self.assertRaises(VertexNotFoundError):
            self.graph.incident_edges_iter("Z")

    def test_bidirectional_navigation_and_bounds(self) -> None:
        """Verify manual forward/backward movement and StopIteration bounds."""
        iterator = self.graph.vertices_iter()
        self.assertFalse(iterator.is_const)
        self.assertFalse(iterator.is_reverse)
        self.assertFalse(iterator.has_prev())

        # До первого шага current() должен бросать InvalidIteratorError
        with self.assertRaises(InvalidIteratorError):
            iterator.current()

        self.assertEqual(iterator.next_item(), "A")
        self.assertEqual(iterator.current(), "A")
        self.assertEqual(iterator.next_item(), "B")
        self.assertTrue(iterator.has_prev())
        self.assertEqual(iterator.prev_item(), "A")

        with self.assertRaises(StopIteration):
            iterator.prev_item()

        iterator.next_item()
        iterator.next_item()
        with self.assertRaises(StopIteration):
            iterator.next_item()

    def test_remove_by_iterator_and_const_protection(self) -> None:
        """Verify removing vertices/edges by iterator and blocking const iterators."""
        edge_iter = self.graph.edges_iter()
        first_edge = edge_iter.next_item()
        self.graph.remove_edge_by_iterator(edge_iter)
        self.assertFalse(self.graph.has_edge(first_edge[0], first_edge[1]))

        vertex_iter = self.graph.vertices_iter()
        first_vertex = vertex_iter.next_item()
        self.graph.remove_vertex_by_iterator(vertex_iter)
        self.assertFalse(self.graph.has_vertex(first_vertex))

        # Константный итератор не должен позволять удаление
        const_iter = self.graph.vertices_iter(const=True)
        const_iter.next_item()
        with self.assertRaises(ConstIteratorError):
            self.graph.remove_vertex_by_iterator(const_iter)

        # Итератор от другого графа должен отклоняться
        other_graph: UndirectedGraph[str] = UndirectedGraph()
        other_graph.add_vertex("X")
        foreign_iter = other_graph.vertices_iter()
        foreign_iter.next_item()
        with self.assertRaises(InvalidIteratorError):
            self.graph.remove_vertex_by_iterator(foreign_iter)


if __name__ == "__main__":
    unittest.main()