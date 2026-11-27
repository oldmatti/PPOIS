"""Custom exceptions package for Lab 4."""

from lab4.exceptions.graph_exceptions import (
    ConstIteratorError,
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    GraphError,
    InvalidIteratorError,
    SelfLoopNotAllowedError,
    VertexAlreadyExistsError,
    VertexNotFoundError,
)

__all__ = [
    "ConstIteratorError",
    "EdgeAlreadyExistsError",
    "EdgeNotFoundError",
    "GraphError",
    "InvalidIteratorError",
    "SelfLoopNotAllowedError",
    "VertexAlreadyExistsError",
    "VertexNotFoundError",
]