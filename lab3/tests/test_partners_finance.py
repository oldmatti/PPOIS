"""Unit tests for partners, shipments, finance, analytics, and WarehouseSystem."""

import pytest

from constants import STATUS_COMPLETED
from exceptions import BudgetExceededError, InvalidDataError, InvalidOrderStateError
from models import (
    Address,
    AnalyticsReport,
    Barcode,
    Carrier,
    Client,
    EquipmentFleet,
    InventoryBatch,
    Invoice,
    OperationDispatcher,
    OrderItem,
    OutboundOrder,
    Pallet,
    Product,
    ProductCategory,
    Shipment,
    StaffScheduler,
    StorageCondition,
    Supplier,
    Warehouse,
    WarehouseBudget,
    WarehouseSystem,
)


def _sample_product() -> Product:
    cat = ProductCategory("C-1", "Gen", StorageCondition())
    return Product("SKU-1", "Item", cat, Barcode("12345", "EAN13"), 5.0, 0.1, 100.0)


def test_supplier_client_and_carrier() -> None:
    """Test Supplier, Client, and Carrier business methods."""
    supplier = Supplier("SUP-1", "Acme", "sales@acme.com", 90.0)
    supplier.register_sku("SKU-1")
    assert "SKU-1" in supplier.supplied_skus
    assert supplier.adjust_reliability(-15.0) == 75.0
    with pytest.raises(InvalidDataError):
        Supplier("SUP-2", "Acme", "invalid-email")
    with pytest.raises(InvalidDataError):
        Supplier("SUP-2", "Acme", "a@b.com", 150.0)

    addr = Address("BY", "Minsk", "Lenina", "1", "220000")
    client = Client("CL-1", "RetailCo", addr, credit_limit=500.0)
    assert client.can_place_order(300.0)
    assert client.add_charge(200.0) == 200.0
    assert not client.can_place_order(400.0)
    with pytest.raises(InvalidDataError):
        client.add_charge(-50.0)
    with pytest.raises(InvalidDataError):
        Client("", "RetailCo", addr, 100.0)

    carrier = Carrier("CAR-1", "FastLog", rate_per_kg=2.5, max_vehicle_load_kg=1000.0)
    assert carrier.can_carry(200.0)
    assert carrier.calculate_shipping_cost(200.0) == 500.0
    with pytest.raises(InvalidDataError):
        carrier.calculate_shipping_cost(-1.0)
    with pytest.raises(InvalidDataError):
        Carrier("", "FastLog", 2.5, 1000.0)


def test_shipment_and_invoice() -> None:
    """Test Shipment dispatch/delivery and Invoice tax calculation."""
    product = _sample_product()
    order = OutboundOrder("OUT-1", "CL-1")
    order.add_item(OrderItem(product, 2))
    carrier = Carrier("CAR-1", "FastLog", rate_per_kg=3.0, max_vehicle_load_kg=500.0)

    pallet = Pallet("PAL-1")
    pallet.load_batch(InventoryBatch("BAT-1", product, 2))
    shipment = Shipment("SHP-1", order, carrier)
    with pytest.raises(InvalidOrderStateError):
        shipment.attach_pallet(pallet)
    pallet.wrap_for_shipping()
    shipment.attach_pallet(pallet)
    assert shipment.dispatch() == 30.0
    shipment.mark_delivered()
    assert shipment.status == STATUS_COMPLETED
    with pytest.raises(InvalidOrderStateError):
        shipment.mark_delivered()
    with pytest.raises(InvalidDataError):
        Shipment("", order, carrier)

    client = Client("CL-1", "RetailCo", Address("BY", "Minsk", "Main", "1", "220000"), 1000.0)
    invoice = Invoice("INV-1", client, order, tax_rate=0.2)
    assert invoice.calculate_subtotal() == 200.0
    assert invoice.calculate_total_with_tax() == 240.0
    invoice.mark_as_paid()
    assert invoice.is_paid
    with pytest.raises(InvalidDataError):
        Invoice("INV-2", client, order, tax_rate=2.0)


def test_budget_report_and_warehouse_system() -> None:
    """Test WarehouseBudget, AnalyticsReport, and WarehouseSystem facade."""
    budget = WarehouseBudget(2026, 1000.0)
    assert budget.allocate_expense("Electricity", 250.0) == 750.0
    with pytest.raises(BudgetExceededError):
        budget.allocate_expense("New Crane", 5000.0)
    with pytest.raises(InvalidDataError):
        budget.allocate_expense("", 10.0)
    with pytest.raises(InvalidDataError):
        WarehouseBudget(1990, 1000.0)

    warehouse = Warehouse("WH-1", "Hub", Address("BY", "Minsk", "Main", "1", "220000"))
    dispatcher = OperationDispatcher("DISP-1")
    report = AnalyticsReport("REP-1", warehouse, dispatcher, budget)
    assert "Hub" in report.generate_summary()
    assert report.calculate_budget_utilization_percent() == 25.0
    with pytest.raises(InvalidDataError):
        AnalyticsReport("", warehouse, dispatcher, budget)

    system = WarehouseSystem(
        warehouse,
        EquipmentFleet("WH-1"),
        StaffScheduler("WH-1"),
        dispatcher,
        budget,
    )
    product = _sample_product()
    system.register_product(product)
    with pytest.raises(InvalidDataError):
        system.register_product(product)
    system.register_batch(InventoryBatch("BAT-1", product, 3))
    system.register_supplier(Supplier("SUP-1", "Acme", "a@b.com"))
    system.register_client(
        Client("CL-1", "Retail", Address("BY", "Minsk", "Main", "1", "220000"), 1000.0)
    )
    assert system.calculate_total_inventory_value() == 300.0