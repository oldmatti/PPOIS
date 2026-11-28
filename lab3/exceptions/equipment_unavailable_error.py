"""Exception for unavailable warehouse equipment."""

from .warehouse_exception import WarehouseException


class EquipmentUnavailableError(WarehouseException):
    """Raised when equipment is busy, discharged, or out of order."""