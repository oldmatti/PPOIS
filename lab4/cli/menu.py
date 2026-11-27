"""Interactive CLI menu demonstrating generic sorting and the undirected graph."""

from __future__ import annotations

from array import array
from typing import Callable, Dict, List

from lab4.exceptions import GraphError
from lab4.graph import UndirectedGraph
from lab4.sorting import Product, bucket_sort, selection_sort


class Lab4CLI:
    """Console interface for interacting with Lab 4 sorting and graph features."""

    def __init__(self) -> None:
        """Initialize the CLI with an empty string-based undirected graph."""
        self._graph: UndirectedGraph[str] = UndirectedGraph()
        self._is_running: bool = True

    def run(self) -> None:
        """Start the main interactive menu loop."""
        actions: Dict[str, Callable[[], None]] = {
            "1": self._demo_sorting,
            "2": self._add_vertex,
            "3": self._add_edge,
            "4": self._remove_vertex,
            "5": self._remove_edge,
            "6": self._show_graph_info,
            "7": self._show_iterators,
            "8": self._show_degrees,
            "9": self._clear_graph,
            "0": self._stop,
        }

        # Основной цикл консольного меню
        while self._is_running:
            self._print_menu()
            choice = input("Select an option: ").strip()
            action = actions.get(choice)
            if action is None:
                print("Unknown option. Please choose a valid number.")
                continue
            self._execute_safely(action)

    def _print_menu(self) -> None:
        """Display available CLI commands."""
        print("\n=== Lab 4: Generic Sorting & Undirected Graph ===")
        print("1. Demonstrate Selection Sort & Bucket Sort")
        print("2. Add vertex to graph")
        print("3. Add edge to graph")
        print("4. Remove vertex from graph")
        print("5. Remove edge from graph")
        print("6. Print graph & counts")
        print("7. Traverse graph with iterators (forward & reverse)")
        print("8. Show vertex degree and edge degree")
        print("9. Clear graph")
        print("0. Exit")

    def _execute_safely(self, action: Callable[[], None]) -> None:
        """Run a menu action and print user-friendly error messages."""
        try:
            action()
        except (GraphError, ValueError, TypeError) as error:
            print(f"Error: {error}")

    def _demo_sorting(self) -> None:
        """Demonstrate Selection Sort and Bucket Sort on built-in and custom types."""
        sample_list: List[int] = [42, 7, 19, 3, 25, 11]
        sample_array = array("d", [3.5, 1.2, 4.8, 0.9, 2.7])
        products: List[Product] = [
            Product("Keyboard", 75.0, 4.6),
            Product("Mouse", 25.5, 4.8),
            Product("Monitor", 299.9, 4.4),
            Product("Headset", 60.0, 4.9),
        ]

        # Демонстрация сортировки встроенных и пользовательских типов
        print("\n--- Built-in list (int) ---")
        print("Original:      ", sample_list)
        print("Selection sort:", selection_sort(sample_list))
        print("Bucket sort:   ", bucket_sort(sample_list))

        print("\n--- Array (array.array) ---")
        print("Original:      ", sample_array)
        print("Selection sort:", selection_sort(sample_array))
        print("Bucket sort:   ", bucket_sort(sample_array))

        print("\n--- Custom class (Product by price / rating) ---")
        print("By price (Selection):", selection_sort(products))
        print(
            "By rating desc (Bucket):",
            bucket_sort(products, key=lambda item: item.rating, reverse=True),
        )

    def _add_vertex(self) -> None:
        """Prompt for a vertex name and add it to the graph."""
        vertex = input("Enter vertex name: ").strip()
        if not vertex:
            raise ValueError("Vertex name cannot be empty.")
        self._graph.add_vertex(vertex)
        print(f"Vertex '{vertex}' added.")

    def _add_edge(self) -> None:
        """Prompt for two vertex names and connect them with an undirected edge."""
        first_vertex = input("Enter first vertex: ").strip()
        second_vertex = input("Enter second vertex: ").strip()
        self._graph.add_edge(first_vertex, second_vertex)
        print(f"Edge ({first_vertex} -- {second_vertex}) added.")

    def _remove_vertex(self) -> None:
        """Prompt for a vertex name and remove it from the graph."""
        vertex = input("Enter vertex to remove: ").strip()
        self._graph.remove_vertex(vertex)
        print(f"Vertex '{vertex}' removed.")

    def _remove_edge(self) -> None:
        """Prompt for two vertex names and remove the edge between them."""
        first_vertex = input("Enter first vertex: ").strip()
        second_vertex = input("Enter second vertex: ").strip()
        self._graph.remove_edge(first_vertex, second_vertex)
        print(f"Edge ({first_vertex} -- {second_vertex}) removed.")

    def _show_graph_info(self) -> None:
        """Print the graph string representation and vertex/edge statistics."""
        print("\nGraph:", self._graph)
        print(f"Vertices: {self._graph.vertex_count()}, Edges: {self._graph.edge_count()}")
        print(f"Is empty: {self._graph.is_empty()}")

    def _show_iterators(self) -> None:
        """Display forward and reverse traversal using graph iterators."""
        forward_vertices = list(self._graph.vertices_iter(const=True))
        reverse_vertices = list(self._graph.vertices_iter(reverse=True, const=True))
        forward_edges = list(self._graph.edges_iter(const=True))
        reverse_edges = list(self._graph.edges_iter(reverse=True, const=True))

        print("\nVertices (forward):", forward_vertices)
        print("Vertices (reverse):", reverse_vertices)
        print("Edges (forward):   ", forward_edges)
        print("Edges (reverse):   ", reverse_edges)

    def _show_degrees(self) -> None:
        """Show the degree of a chosen vertex and optionally an edge."""
        vertex = input("Enter vertex for degree check: ").strip()
        print(f"Degree of '{vertex}': {self._graph.vertex_degree(vertex)}")
        neighbors = list(self._graph.adjacent_vertices_iter(vertex, const=True))
        print(f"Adjacent vertices: {neighbors}")

        second_vertex = input("Enter neighbor for edge degree (or leave blank): ").strip()
        if second_vertex:
            degree = self._graph.edge_degree(vertex, second_vertex)
            print(f"Degree of edge ({vertex} -- {second_vertex}): {degree}")

    def _clear_graph(self) -> None:
        """Clear all vertices and edges from the graph."""
        self._graph.clear()
        print("Graph cleared.")

    def _stop(self) -> None:
        """Stop the interactive menu loop."""
        self._is_running = False
        print("Exiting Lab 4 CLI.")