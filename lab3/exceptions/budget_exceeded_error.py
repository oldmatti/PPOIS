"""Exception for warehouse budget overflow."""

from .warehouse_exception import WarehouseException


class BudgetExceededError(WarehouseException):
    """Raised when an expense exceeds the available warehouse budget."""