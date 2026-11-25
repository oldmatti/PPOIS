"""Unit tests for warehouse equipment and fleet models."""

import pytest

from exceptions import (
    EquipmentOverloadError,
    EquipmentUnavailableError,
    InvalidDataError,
    TemperatureViolationError,
)
from models import (
    Barcode,
    BarcodeScanner,
    ConveyorBelt,
    EquipmentFleet,
    Forklift,
    InventoryBatch,
    MaintenanceRecord,
    Pallet,
    Product,
    ProductCategory,
    StorageCondition,
    StorageZone,
    TemperatureSensor,
    WarehouseEquipment,
    WeighingScale,
)


def _sample_pallet(weight_per_unit: float = 10.0, qty: int = 5) -> Pallet:
    cat = ProductCategory("C-1", "Gen", StorageCondition())
    product = Product("SKU-1", "Item", cat, Barcode("12345", "EAN13"), weight_per_unit, 0.1, 10.0)
    pallet = Pallet("PAL-1", max_weight_kg=5000.0)
    pallet.load_batch(InventoryBatch("BAT-1", product, qty))
    return pallet


def test_maintenance_record_and_base_equipment() -> None:
    """Test MaintenanceRecord and WarehouseEquipment lifecycle."""
    record = MaintenanceRecord("MR-1", "EQ-1", "Motor replacement", 1500.0)
    assert record.is_major_repair(1000.0)
    record.complete_maintenance()
    assert record.is_completed
    with pytest.raises(InvalidDataError):
        record.is_major_repair(-10.0)
    with pytest.raises(InvalidDataError):
        MaintenanceRecord("", "EQ-1", "Fix", 10.0)

    equip = WarehouseEquipment("EQ-1", "Generic-X")
    equip.checkout()
    with pytest.raises(EquipmentUnavailableError):
        equip.checkout()
    equip.release()
    equip.log_maintenance(record)
    assert not equip.is_operational
    equip.restore_to_service()
    assert equip.is_operational
    with pytest.raises(InvalidDataError):
        WarehouseEquipment("", "Generic-X")


def test_forklift_and_barcode_scanner() -> None:
    """Test Forklift lifting/charging and BarcodeScanner operations."""
    forklift = Forklift("FL-1", "Toyota", max_load_kg=100.0, battery_percent=20.0)
    light_pallet = _sample_pallet(10.0, 5)
    heavy_pallet = _sample_pallet(50.0, 5)
    forklift.lift_pallet(light_pallet, battery_cost=10.0)
    assert forklift.battery_percent == 10.0
    with pytest.raises(EquipmentUnavailableError):
        forklift.lift_pallet(light_pallet)
    assert forklift.charge_battery(50.0) == 60.0
    with pytest.raises(EquipmentOverloadError):
        forklift.lift_pallet(heavy_pallet)
    with pytest.raises(InvalidDataError):
        forklift.charge_battery(0.0)
    with pytest.raises(InvalidDataError):
        Forklift("FL-2", "Toyota", max_load_kg=-10.0)

    scanner = BarcodeScanner("SC-1", "Zebra")
    assert scanner.scan_barcode(Barcode("4810001234567", "EAN13"))
    assert not scanner.scan_barcode(Barcode("ABC", "EAN13"))
    assert scanner.clear_scan_history() == 1
    scanner.is_operational = False
    with pytest.raises(EquipmentUnavailableError):
        scanner.scan_barcode(Barcode("12345", "EAN13"))


def test_conveyor_sensor_scale_and_fleet() -> None:
    """Test ConveyorBelt, TemperatureSensor, WeighingScale, and EquipmentFleet."""
    belt = ConveyorBelt("CB-1", "BeltPro", max_weight_kg=50.0, max_speed_mps=2.0)
    with pytest.raises(EquipmentUnavailableError):
        belt.transport_load(10.0)
    belt.start_belt(1.5)
    assert belt.transport_load(30.0)
    with pytest.raises(EquipmentOverloadError):
        belt.transport_load(80.0)
    belt.stop_belt()
    with pytest.raises(InvalidDataError):
        belt.start_belt(5.0)
    belt.is_operational = False
    with pytest.raises(EquipmentUnavailableError):
        belt.start_belt(1.0)
    with pytest.raises(InvalidDataError):
        ConveyorBelt("CB-2", "BeltPro", -1.0, 2.0)

    zone = StorageZone("Z-1", "Cool", StorageCondition(2.0, 8.0))
    sensor = TemperatureSensor("TS-1", "Thermo", zone)
    sensor.record_reading(5.0)
    assert sensor.calibrate(0.5) == 5.5
    with pytest.raises(TemperatureViolationError):
        sensor.record_reading(25.0)
    sensor.is_operational = False
    with pytest.raises(EquipmentUnavailableError):
        sensor.record_reading(5.0)

    scale = WeighingScale("WS-1", "Mettler", max_capacity_kg=100.0)
    assert scale.weigh_pallet(_sample_pallet(10.0, 5)) == 50.0
    scale.reset_tare()
    assert scale.last_weight_kg == 0.0
    with pytest.raises(EquipmentOverloadError):
        scale.weigh_pallet(_sample_pallet(50.0, 5))
    scale.is_operational = False
    with pytest.raises(EquipmentUnavailableError):
        scale.weigh_pallet(_sample_pallet(10.0, 1))
    with pytest.raises(InvalidDataError):
        WeighingScale("WS-2", "Mettler", 0.0)

    fleet = EquipmentFleet("WH-1")
    fl = Forklift("FL-9", "Linde")
    fl.log_maintenance(MaintenanceRecord("MR-2", "FL-9", "Battery", 300.0))
    fl.restore_to_service()
    fleet.register_equipment(fl)
    assert fleet.find_available_by_type(Forklift) is fl
    assert fleet.find_available_by_type(BarcodeScanner) is None
    assert fleet.calculate_total_maintenance_cost() == 300.0
    with pytest.raises(InvalidDataError):
        EquipmentFleet("")