"""Exception for unauthorized warehouse operations."""

from .warehouse_exception import WarehouseException


class UnauthorizedAccessError(WarehouseException):
    """Raised when an employee lacks required permissions for an action."""