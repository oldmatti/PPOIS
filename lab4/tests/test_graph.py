"""Unit tests for the generic UndirectedGraph container."""

import unittest

from lab4.constants import EMPTY_GRAPH_LABEL
from lab4.exceptions import (
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    SelfLoopNotAllowedError,
    VertexAlreadyExistsError,
    VertexNotFoundError,
)
from lab4.graph import UndirectedGraph


class TestUndirectedGraph(unittest.TestCase):
    """Tests for core operations of UndirectedGraph."""

    def setUp(self) -> None:
        """Create a sample undirected graph before each test."""
        self.graph: UndirectedGraph[str] = UndirectedGraph()
        for vertex in ("A", "B", "C", "D"):
            self.graph.add_vertex(vertex)
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        self.graph.add_edge("A", "C")

    def test_empty_and_clear(self) -> None:
        """Verify is_empty, clear, and empty string representation."""
        empty_graph: UndirectedGraph[int] = UndirectedGraph()
        self.assertTrue(empty_graph.is_empty())
        self.assertEqual(str(empty_graph), EMPTY_GRAPH_LABEL)

        self.assertFalse(self.graph.is_empty())
        self.graph.clear()
        self.assertTrue(self.graph.is_empty())
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_counts_existence_and_degrees(self) -> None:
        """Verify vertex/edge counts, existence checks, and degrees."""
        self.assertEqual(self.graph.vertex_count(), 4)
        self.assertEqual(self.graph.edge_count(), 3)
        self.assertTrue(self.graph.has_vertex("A"))
        self.assertFalse(self.graph.has_vertex("Z"))
        self.assertTrue(self.graph.has_edge("A", "B"))
        self.assertTrue(self.graph.has_edge("B", "A"))
        self.assertFalse(self.graph.has_edge("A", "D"))
        self.assertFalse(self.graph.has_edge("A", "Z"))

        # Проверка степеней вершин и рёбер
        self.assertEqual(self.graph.vertex_degree("A"), 2)
        self.assertEqual(self.graph.vertex_degree("D"), 0)
        self.assertEqual(self.graph.edge_degree("A", "B"), 2)

    def test_remove_vertex_and_edge(self) -> None:
        """Verify removing edges and vertices updates adjacency correctly."""
        self.graph.remove_edge("A", "C")
        self.assertFalse(self.graph.has_edge("A", "C"))
        self.assertEqual(self.graph.edge_count(), 2)

        self.graph.remove_vertex("B")
        self.assertFalse(self.graph.has_vertex("B"))
        self.assertEqual(self.graph.vertex_count(), 3)
        self.assertEqual(self.graph.edge_count(), 0)

    def test_copy_and_assign_from(self) -> None:
        """Verify deep copy and assign_from isolate graph state."""
        cloned = self.graph.copy()
        self.assertEqual(cloned, self.graph)

        cloned.add_vertex("E")
        self.assertFalse(self.graph.has_vertex("E"))
        self.assertNotEqual(cloned, self.graph)

        target: UndirectedGraph[str] = UndirectedGraph()
        target.assign_from(self.graph)
        self.assertEqual(target, self.graph)

        with self.assertRaises(TypeError):
            target.assign_from("invalid")  # type: ignore[arg-type]

    def test_comparisons_and_string_output(self) -> None:
        """Verify comparison operators and iterator-based __str__."""
        smaller: UndirectedGraph[str] = UndirectedGraph()
        smaller.add_vertex("A")

        self.assertLess(smaller, self.graph)
        self.assertLessEqual(smaller, self.graph)
        self.assertGreater(self.graph, smaller)
        self.assertGreaterEqual(self.graph, smaller)
        self.assertNotEqual(self.graph, "not a graph")

        text = str(self.graph)
        self.assertIn("UndirectedGraph", text)
        self.assertIn("'A'", text)
        self.assertIn("'B'", text)

    def test_graph_exceptions(self) -> None:
        """Verify all custom graph exceptions are raised on invalid operations."""
        with self.assertRaises(VertexAlreadyExistsError):
            self.graph.add_vertex("A")
        with self.assertRaises(VertexNotFoundError):
            self.graph.remove_vertex("Z")
        with self.assertRaises(VertexNotFoundError):
            self.graph.vertex_degree("Z")
        with self.assertRaises(VertexNotFoundError):
            self.graph.add_edge("A", "Z")
        with self.assertRaises(SelfLoopNotAllowedError):
            self.graph.add_edge("A", "A")
        with self.assertRaises(EdgeAlreadyExistsError):
            self.graph.add_edge("B", "A")
        with self.assertRaises(EdgeNotFoundError):
            self.graph.remove_edge("A", "D")
        with self.assertRaises(EdgeNotFoundError):
            self.graph.edge_degree("A", "D")


if __name__ == "__main__":
    unittest.main()
