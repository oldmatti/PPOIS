"""Exception for missing orders in the system."""

from .warehouse_exception import WarehouseException


class OrderNotFoundError(WarehouseException):
    """Raised when an order with the specified identifier is not found."""