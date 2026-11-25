"""Unit tests for warehouse infrastructure models."""

import pytest

from exceptions import (
    BinCapacityExceededError,
    DockOccupiedError,
    InsufficientStockError,
    InvalidDataError,
    TemperatureViolationError,
    UnauthorizedAccessError,
)
from models import (
    Address,
    LoadingDock,
    Rack,
    SecurityCheckpoint,
    Shelf,
    StorageBin,
    StorageCondition,
    StorageZone,
    Warehouse,
)


def test_address_operations_and_validation() -> None:
    """Test address formatting, city comparison, and postal code validation."""
    addr1 = Address("Belarus", "Minsk", "Lenina", "10", "220-013")
    addr2 = Address("Belarus", "minsk", "Pobedy", "5", "220000")
    assert "Minsk" in addr1.format_full_address()
    assert addr1.is_same_city(addr2)
    assert addr1.validate_postal_code()
    with pytest.raises(InvalidDataError):
        Address("", "Minsk", "Lenina", "10", "220013")


def test_storage_condition_bounds_and_compatibility() -> None:
    """Test temperature bounds, compatibility, and validation errors."""
    dry = StorageCondition(10.0, 25.0)
    cool = StorageCondition(5.0, 15.0)
    frozen = StorageCondition(-20.0, -5.0)
    assert dry.is_temperature_acceptable(18.0)
    assert dry.is_compatible_with(cool)
    assert not dry.is_compatible_with(frozen)
    with pytest.raises(InvalidDataError):
        StorageCondition(30.0, 10.0)
    with pytest.raises(InvalidDataError):
        StorageCondition(-50.0, 10.0)


def test_storage_bin_add_remove_and_limits() -> None:
    """Test adding, removing, fill ratio, and capacity errors in StorageBin."""
    storage_bin = StorageBin("B-01", max_weight_kg=100.0, max_volume_m3=2.0)
    storage_bin.add_item("SKU-1", 5, 50.0, 1.0)
    assert storage_bin.calculate_fill_ratio() == 0.5
    with pytest.raises(BinCapacityExceededError):
        storage_bin.add_item("SKU-2", 1, 60.0, 0.5)
    with pytest.raises(BinCapacityExceededError):
        storage_bin.add_item("SKU-2", 1, 10.0, 1.5)
    with pytest.raises(InvalidDataError):
        storage_bin.add_item("SKU-2", 0, 1.0, 0.1)
    storage_bin.remove_item("SKU-1", 5, 50.0, 1.0)
    assert "SKU-1" not in storage_bin.items
    with pytest.raises(InsufficientStockError):
        storage_bin.remove_item("SKU-1", 1, 10.0, 0.2)
    with pytest.raises(InvalidDataError):
        StorageBin("", 100.0, 2.0)


def test_shelf_rack_zone_and_warehouse_hierarchy() -> None:
    """Test Shelf, Rack, StorageZone, and Warehouse aggregation."""
    storage_bin = StorageBin("B-01", 100.0, 2.0)
    storage_bin.add_item("SKU-1", 2, 20.0, 0.4)
    shelf = Shelf("S-01", 1, max_bins=1)
    shelf.add_bin(storage_bin)
    assert shelf.find_bin_with_sku("SKU-1") is storage_bin
    assert shelf.find_bin_with_sku("MISSING") is None
    assert shelf.calculate_total_weight() == 20.0
    with pytest.raises(InvalidDataError):
        shelf.add_bin(StorageBin("B-02"))
    with pytest.raises(InvalidDataError):
        Shelf("", 1, 1)

    rack = Rack("R-01", "A1", max_shelves=1)
    rack.add_shelf(shelf)
    assert rack.find_available_bin(50.0) is storage_bin
    assert rack.find_available_bin(500.0) is None
    assert rack.calculate_total_load() == 20.0
    with pytest.raises(InvalidDataError):
        rack.add_shelf(Shelf("S-02", 2, 1))
    with pytest.raises(InvalidDataError):
        Rack("", "A1", 1)

    zone = StorageZone("Z-01", "Main", StorageCondition(10.0, 25.0))
    zone.add_rack(rack)
    assert zone.count_total_bins() == 1
    zone.update_temperature(20.0)
    with pytest.raises(TemperatureViolationError):
        zone.update_temperature(35.0)
    with pytest.raises(InvalidDataError):
        StorageZone("", "Main", StorageCondition())

    warehouse = Warehouse("WH-1", "Hub", Address("BY", "Minsk", "Main", "1", "220000"))
    warehouse.add_zone(zone)
    assert warehouse.get_total_bin_count() == 1
    with pytest.raises(InvalidDataError):
        Warehouse("", "Hub", Address("BY", "Minsk", "Main", "1", "220000"))


def test_loading_dock_and_security_checkpoint() -> None:
    """Test LoadingDock states, Warehouse dock lookup, and SecurityCheckpoint."""
    dock = LoadingDock("D-01", "inbound")
    dock.assign_vehicle("AB-1234")
    with pytest.raises(DockOccupiedError):
        dock.assign_vehicle("CD-5678")
    with pytest.raises(DockOccupiedError):
        dock.set_maintenance_mode(True)
    assert dock.release_vehicle() == "AB-1234"
    dock.set_maintenance_mode(True)
    with pytest.raises(DockOccupiedError):
        dock.assign_vehicle("EF-9012")
    dock.set_maintenance_mode(False)
    with pytest.raises(InvalidDataError):
        LoadingDock("D-02", "invalid")

    warehouse = Warehouse("WH-1", "Hub", Address("BY", "Minsk", "Main", "1", "220000"))
    warehouse.add_dock(dock)
    assert warehouse.find_free_dock("inbound") is dock
    assert warehouse.find_free_dock("outbound") is None

    checkpoint = SecurityCheckpoint("CP-01", required_clearance=3)
    assert checkpoint.verify_entry("BADGE-1", 3)
    checkpoint.log_vehicle_passage("AB-1234", "in")
    with pytest.raises(InvalidDataError):
        checkpoint.log_vehicle_passage("AB-1234", "sideways")
    with pytest.raises(UnauthorizedAccessError):
        checkpoint.verify_entry("BADGE-2", 1)
    checkpoint.is_active = False
    with pytest.raises(UnauthorizedAccessError):
        checkpoint.verify_entry("BADGE-1", 5)
    with pytest.raises(InvalidDataError):
        SecurityCheckpoint("", 1)