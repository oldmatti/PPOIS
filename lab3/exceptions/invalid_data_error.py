"""Exception for invalid input data."""

from .warehouse_exception import WarehouseException


class InvalidDataError(WarehouseException):
    """Raised when invalid values are passed to a model."""