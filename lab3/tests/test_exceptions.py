"""Unit tests for custom warehouse exception hierarchy."""

import pytest

from exceptions import (
    BinCapacityExceededError,
    BudgetExceededError,
    DockOccupiedError,
    EquipmentOverloadError,
    EquipmentUnavailableError,
    ExpiredProductError,
    InsufficientStockError,
    InvalidDataError,
    InvalidOrderStateError,
    OrderNotFoundError,
    QualityCheckFailedError,
    TemperatureViolationError,
    UnauthorizedAccessError,
    WarehouseException,
)


@pytest.mark.parametrize(
    "exc_cls",
    [
        InvalidDataError,
        InsufficientStockError,
        BinCapacityExceededError,
        TemperatureViolationError,
        ExpiredProductError,
        EquipmentUnavailableError,
        EquipmentOverloadError,
        UnauthorizedAccessError,
        OrderNotFoundError,
        InvalidOrderStateError,
        DockOccupiedError,
        QualityCheckFailedError,
        BudgetExceededError,
    ],
)
def test_exception_inherits_from_warehouse_exception(exc_cls) -> None:
    """Verify every custom exception inherits from WarehouseException."""
    error = exc_cls("test message")
    assert isinstance(error, WarehouseException)
    assert str(error) == "test message"