"""Exception for failed quality inspections."""

from .warehouse_exception import WarehouseException


class QualityCheckFailedError(WarehouseException):
    """Raised when a product batch fails quality inspection."""