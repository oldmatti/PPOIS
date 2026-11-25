"""Exception for storage temperature regime violations."""

from .warehouse_exception import WarehouseException


class TemperatureViolationError(WarehouseException):
    """Raised when temperature does not match required storage conditions."""