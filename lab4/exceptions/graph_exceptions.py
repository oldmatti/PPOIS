"""Custom exception hierarchy for the undirected graph container."""


class GraphError(Exception):
    """Base exception for all graph-related errors."""


class VertexAlreadyExistsError(GraphError):
    """Raised when attempting to add a duplicate vertex."""


class VertexNotFoundError(GraphError):
    """Raised when a requested vertex does not exist in the graph."""


class EdgeAlreadyExistsError(GraphError):
    """Raised when attempting to add a duplicate edge."""


class EdgeNotFoundError(GraphError):
    """Raised when a requested edge does not exist in the graph."""


class SelfLoopNotAllowedError(GraphError):
    """Raised when attempting to add a self-loop edge in a simple graph."""


class InvalidIteratorError(GraphError):
    """Raised when an iterator is out of bounds or does not match the graph."""


class ConstIteratorError(GraphError):
    """Raised when attempting to modify the graph through a read-only iterator."""