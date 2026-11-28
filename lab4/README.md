# Laboratory Work 4: Generic Programming — Sorting & Graph Container

## Overview

This laboratory work implements Variant 5 in Python 3.9+ using generic typing (`typing.TypeVar`, `typing.Generic`) and strict encapsulation:

1. **Task 1 — Generic Sorting Algorithms:**
   - **Selection Sort** (`selection_sort`)
   - **Bucket Sort** (`bucket_sort`)
   - Supports both standard dynamic lists (`list`) and typed arrays (`array.array`) as well as tuples, preserving the input collection type.
   - Includes a custom domain class `Product` to demonstrate sorting user-defined objects alongside built-in types (`int`, `float`).

2. **Task 2 — Generic Undirected Graph (`UndirectedGraph[VertexValue]`):**
   - Backed by an encapsulated adjacency list (internal representation is hidden).
   - Supports default construction, deep copy (`copy`), copy assignment (`assign_from`), emptiness check (`is_empty`), clearing (`clear`), and full comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`).
   - Supports vertex/edge insertion, removal, existence checks, counts, vertex degree, edge degree, and iterator-based removal.
   - Provides **bidirectional iterators** (`BidirectionalIterator`) with **reverse** and **const (read-only)** modes for vertices, edges, incident edges, and adjacent vertices.
   - Builds `__str__` strictly via constant graph iterators.

## Project Structure

- `constants.py` — named configuration constants
- `exceptions/` — custom graph and iterator exception hierarchy
- `sorting/` — `selection_sort`, `bucket_sort`, and `Product`
- `graph/` — `UndirectedGraph` container and `BidirectionalIterator`
- `cli/` — interactive console menu separated from domain logic
- `tests/` — unit tests with >90% coverage
- `main.py` — CLI entry point

## Usage

Run the interactive CLI from the repository root:

```bash
python3 -m lab4.main