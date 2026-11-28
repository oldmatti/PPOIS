"""Unit tests for warehouse personnel and scheduling models."""

import pytest

from exceptions import InvalidDataError, QualityCheckFailedError, UnauthorizedAccessError
from models import (
    AccessBadge,
    Barcode,
    Employee,
    ForkliftOperator,
    InventoryBatch,
    Product,
    ProductCategory,
    QualityInspector,
    Shift,
    StaffScheduler,
    StorageBin,
    StorageCondition,
    Storekeeper,
    WarehouseManager,
)


def test_access_badge_and_shift() -> None:
    """Test AccessBadge upgrades/deactivation and Shift extensions."""
    badge = AccessBadge("B-1", clearance_level=2)
    badge.upgrade_clearance(4)
    assert badge.clearance_level == 4
    badge.deactivate()
    with pytest.raises(InvalidDataError):
        badge.upgrade_clearance(5)
    with pytest.raises(InvalidDataError):
        AccessBadge("", 1)

    shift = Shift("SH-1", "day", duration_hours=8)
    shift.extend_shift(2)
    assert shift.duration_hours == 10
    with pytest.raises(InvalidDataError):
        shift.extend_shift(5)
    shift.close_shift()
    with pytest.raises(InvalidDataError):
        shift.extend_shift(1)
    with pytest.raises(InvalidDataError):
        Shift("SH-2", "invalid", 8)
    with pytest.raises(InvalidDataError):
        Shift("SH-2", "day", 20)


def test_employee_and_specialized_roles() -> None:
    """Test Employee, Storekeeper, ForkliftOperator, QualityInspector, and WarehouseManager."""
    badge = AccessBadge("B-2", clearance_level=3)
    emp = Employee("E-1", "Ivan Ivanov", "worker", 20.0, badge)
    emp.log_work_hours(8.0)
    assert emp.calculate_pay() == 160.0
    assert emp.verify_clearance(3)
    with pytest.raises(UnauthorizedAccessError):
        emp.verify_clearance(5)
    with pytest.raises(InvalidDataError):
        emp.log_work_hours(0)
    with pytest.raises(InvalidDataError):
        Employee("", "Ivan", "worker", 20.0, badge)

    keeper = Storekeeper("E-2", "Anna Petrova", 22.0, badge, "Z-A")
    storage_bin = StorageBin("B-01")
    keeper.place_in_bin(storage_bin, "SKU-1", 4, 10.0, 0.2)
    keeper.record_completed_pick("PICK-1")
    assert len(keeper.completed_picks) == 1

    operator = ForkliftOperator("E-3", "Petr Sidorov", 25.0, badge, "LIC-99")
    operator.record_pallet_move()
    assert operator.pallets_moved == 1
    operator.suspend_license()
    with pytest.raises(UnauthorizedAccessError):
        operator.record_pallet_move()
    with pytest.raises(InvalidDataError):
        ForkliftOperator("E-3", "Petr", 25.0, badge, "")

    inspector = QualityInspector("E-4", "Olga Smirnova", 30.0, badge, "CERT-1")
    cat = ProductCategory("C-1", "Gen", StorageCondition())
    batch = InventoryBatch("BAT-1", Product("SKU-1", "Item", cat, Barcode("123", "EAN13"), 1.0, 0.1, 10.0), 5)
    assert inspector.inspect_batch(batch, 2.0)
    with pytest.raises(QualityCheckFailedError):
        inspector.inspect_batch(batch, 12.0)
    assert batch.is_quarantined

    manager = WarehouseManager("E-5", "Sergey Volkov", 40.0, badge, approval_limit=5000.0)
    manager.add_subordinate(emp)
    assert manager.approve_expense(1000.0)
    assert manager.calculate_team_payroll() == 160.0
    with pytest.raises(UnauthorizedAccessError):
        manager.approve_expense(9000.0)


def test_staff_scheduler() -> None:
    """Test StaffScheduler shift assignments and duplicate prevention."""
    scheduler = StaffScheduler("WH-1")
    shift = Shift("SH-1", "night", 8)
    emp = Employee("E-1", "Ivan", "worker", 20.0, AccessBadge("B-1", 2))
    scheduler.assign_employee_to_shift(shift, emp)
    assert scheduler.get_shift_headcount("SH-1") == 1
    with pytest.raises(InvalidDataError):
        scheduler.assign_employee_to_shift(shift, emp)
    shift.close_shift()
    with pytest.raises(InvalidDataError):
        scheduler.assign_employee_to_shift(shift, Employee("E-2", "Anna", "worker", 20.0, AccessBadge("B-2", 2)))
    with pytest.raises(InvalidDataError):
        StaffScheduler("")