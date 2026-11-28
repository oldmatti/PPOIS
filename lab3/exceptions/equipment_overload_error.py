"""Exception for warehouse equipment overload."""

from .warehouse_exception import WarehouseException


class EquipmentOverloadError(WarehouseException):
    """Raised when equipment load capacity is exceeded."""