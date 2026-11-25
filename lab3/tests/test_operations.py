"""Unit tests for warehouse operations and order models."""

import pytest

from constants import STATUS_CANCELLED, STATUS_COMPLETED, STATUS_FAILED
from exceptions import (
    InvalidDataError,
    InvalidOrderStateError,
    OrderNotFoundError,
    QualityCheckFailedError,
)
from models import (
    AccessBadge,
    Barcode,
    InboundOrder,
    InventoryAudit,
    InventoryBatch,
    OperationDispatcher,
    OrderItem,
    OutboundOrder,
    PackingStation,
    Pallet,
    PickingTask,
    Product,
    ProductCategory,
    QualityCheck,
    QualityInspector,
    ReturnRequest,
    StockTransfer,
    StorageBin,
    StorageCondition,
    Storekeeper,
)


def _sample_product() -> Product:
    cat = ProductCategory("C-1", "Gen", StorageCondition())
    return Product("SKU-1", "Widget", cat, Barcode("12345", "EAN13"), 2.0, 0.1, 25.0)


def test_inbound_and_outbound_orders() -> None:
    """Test OrderItem, InboundOrder, OutboundOrder, and OperationDispatcher."""
    product = _sample_product()
    item = OrderItem(product, 4)
    assert item.calculate_line_total() == 100.0
    assert item.calculate_line_weight() == 8.0
    with pytest.raises(InvalidDataError):
        OrderItem(product, 0)

    inbound = InboundOrder("IN-1", "SUP-1")
    with pytest.raises(InvalidOrderStateError):
        inbound.start_receiving()
    inbound.add_item(item)
    assert inbound.calculate_total_cost() == 100.0
    inbound.start_receiving()
    with pytest.raises(InvalidOrderStateError):
        inbound.add_item(item)
    inbound.complete_receiving()
    assert inbound.status == STATUS_COMPLETED
    with pytest.raises(InvalidOrderStateError):
        inbound.cancel_order()
    with pytest.raises(InvalidDataError):
        InboundOrder("", "SUP-1")

    outbound = OutboundOrder("OUT-1", "CL-1", priority=2)
    outbound.add_item(item)
    assert outbound.calculate_total_weight() == 8.0
    outbound.start_fulfillment()
    outbound.mark_shipped()
    with pytest.raises(InvalidOrderStateError):
        outbound.cancel_order()
    with pytest.raises(InvalidDataError):
        OutboundOrder("OUT-2", "CL-1", priority=9)

    cancelled_out = OutboundOrder("OUT-3", "CL-1")
    cancelled_out.cancel_order()
    assert cancelled_out.status == STATUS_CANCELLED

    dispatcher = OperationDispatcher("DISP-1")
    dispatcher.register_inbound_order(inbound)
    dispatcher.register_outbound_order(outbound)
    dispatcher.register_outbound_order(cancelled_out)
    assert dispatcher.get_outbound_order("OUT-1") is outbound
    assert dispatcher.count_pending_outbound() == 1
    with pytest.raises(OrderNotFoundError):
        dispatcher.get_outbound_order("MISSING")


def test_picking_packing_and_quality_check() -> None:
    """Test PickingTask, PackingStation, and QualityCheck workflows."""
    product = _sample_product()
    order = OutboundOrder("OUT-1", "CL-1")
    source_bin = StorageBin("B-1")
    source_bin.add_item("SKU-1", 5, 10.0, 0.5)
    keeper = Storekeeper("E-1", "Anna", 20.0, AccessBadge("BG-1", 2), "Z-1")

    task = PickingTask("PK-1", order, source_bin, keeper)
    with pytest.raises(InvalidOrderStateError):
        task.complete_picking("SKU-1", 2, 4.0, 0.2)
    task.start_picking()
    with pytest.raises(InvalidOrderStateError):
        task.start_picking()
    task.complete_picking("SKU-1", 2, 4.0, 0.2)
    assert task.status == STATUS_COMPLETED
    assert "PK-1" in keeper.completed_picks
    with pytest.raises(InvalidDataError):
        PickingTask("", order, source_bin, keeper)

    station = PackingStation("PS-1", max_daily_pallets=1)
    pallet = Pallet("PAL-1")
    pallet.load_batch(InventoryBatch("BAT-1", product, 2))
    station.pack_pallet(pallet)
    with pytest.raises(InvalidDataError):
        station.pack_pallet(pallet)
    assert station.reset_daily_counter() == 1
    with pytest.raises(InvalidDataError):
        PackingStation("", 1)

    inspector = QualityInspector("E-2", "Olga", 30.0, AccessBadge("BG-2", 3), "CERT")
    batch = InventoryBatch("BAT-2", product, 10)
    qc = QualityCheck("QC-1", batch, inspector)
    assert qc.execute_check(1.0)
    with pytest.raises(InvalidDataError):
        qc.execute_check(120.0)
    with pytest.raises(QualityCheckFailedError):
        qc.execute_check(15.0)
    assert qc.status == STATUS_FAILED
    with pytest.raises(InvalidDataError):
        QualityCheck("", batch, inspector)


def test_transfer_audit_and_return_request() -> None:
    """Test StockTransfer, InventoryAudit, and ReturnRequest."""
    bin_a = StorageBin("B-A")
    bin_b = StorageBin("B-B")
    bin_a.add_item("SKU-1", 10, 20.0, 1.0)

    transfer = StockTransfer("TR-1", bin_a, bin_b, "SKU-1", 4)
    transfer.execute(2.0, 0.1)
    assert bin_b.items["SKU-1"] == 4
    with pytest.raises(InvalidOrderStateError):
        transfer.execute(2.0, 0.1)
    with pytest.raises(InvalidDataError):
        StockTransfer("TR-2", bin_a, bin_a, "SKU-1", 1)

    audit = InventoryAudit("AUD-1", bin_a, "EMP-9")
    diff = audit.run_audit({"SKU-1": 5, "SKU-2": 1})
    assert audit.has_discrepancies()
    assert diff["SKU-1"] == -1
    assert diff["SKU-2"] == 1
    with pytest.raises(InvalidDataError):
        InventoryAudit("", bin_a, "EMP-9")

    order = OutboundOrder("OUT-9", "CL-1")
    ret = ReturnRequest("RET-1", order, "SKU-1", 1, "Damaged box")
    ret.approve_return()
    assert ret.status == STATUS_COMPLETED
    with pytest.raises(InvalidOrderStateError):
        ret.reject_return()
    ret2 = ReturnRequest("RET-2", order, "SKU-1", 1, "Wrong item")
    ret2.reject_return()
    assert ret2.status == STATUS_CANCELLED
    with pytest.raises(InvalidDataError):
        ReturnRequest("", order, "SKU-1", 1, "Reason")