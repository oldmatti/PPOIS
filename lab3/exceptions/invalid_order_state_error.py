"""Exception for invalid order status transitions."""

from .warehouse_exception import WarehouseException


class InvalidOrderStateError(WarehouseException):
    """Raised when attempting an invalid order state transition."""