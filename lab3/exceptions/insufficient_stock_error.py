"""Exception for insufficient warehouse stock."""

from .warehouse_exception import WarehouseException


class InsufficientStockError(WarehouseException):
    """Raised when the requested quantity exceeds available stock."""