"""Exception for attempting to use an occupied loading dock."""

from .warehouse_exception import WarehouseException


class DockOccupiedError(WarehouseException):
    """Raised when a loading dock is already occupied by another vehicle."""