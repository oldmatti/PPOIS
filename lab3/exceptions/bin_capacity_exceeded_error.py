"""Exception for storage bin capacity overflow."""

from .warehouse_exception import WarehouseException


class BinCapacityExceededError(WarehouseException):
    """Raised when a storage bin weight or volume limit is exceeded."""