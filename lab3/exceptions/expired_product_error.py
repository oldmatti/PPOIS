"""Exception for operations involving expired products."""

from .warehouse_exception import WarehouseException


class ExpiredProductError(WarehouseException):
    """Raised when attempting an operation with an expired batch."""