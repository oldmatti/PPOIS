"""Custom exceptions package for the warehouse management system."""

from .bin_capacity_exceeded_error import BinCapacityExceededError
from .budget_exceeded_error import BudgetExceededError
from .dock_occupied_error import DockOccupiedError
from .equipment_overload_error import EquipmentOverloadError
from .equipment_unavailable_error import EquipmentUnavailableError
from .expired_product_error import ExpiredProductError
from .insufficient_stock_error import InsufficientStockError
from .invalid_data_error import InvalidDataError
from .invalid_order_state_error import InvalidOrderStateError
from .order_not_found_error import OrderNotFoundError
from .quality_check_failed_error import QualityCheckFailedError
from .temperature_violation_error import TemperatureViolationError
from .unauthorized_access_error import UnauthorizedAccessError
from .warehouse_exception import WarehouseException

__all__ = [
    "WarehouseException",
    "InvalidDataError",
    "InsufficientStockError",
    "BinCapacityExceededError",
    "TemperatureViolationError",
    "ExpiredProductError",
    "EquipmentUnavailableError",
    "EquipmentOverloadError",
    "UnauthorizedAccessError",
    "OrderNotFoundError",
    "InvalidOrderStateError",
    "DockOccupiedError",
    "QualityCheckFailedError",
    "BudgetExceededError",
]