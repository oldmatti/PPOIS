"""Unit tests for product and inventory models."""

from datetime import date

import pytest

from exceptions import (
    BinCapacityExceededError,
    ExpiredProductError,
    InsufficientStockError,
    InvalidDataError,
)
from models import (
    Barcode,
    FragileProduct,
    HazardousProduct,
    InventoryBatch,
    Pallet,
    PerishableProduct,
    Product,
    ProductCategory,
    StockRecord,
    StorageBin,
    StorageCondition,
)


def _sample_category() -> ProductCategory:
    return ProductCategory("CAT-1", "General", StorageCondition(10.0, 25.0))


def test_category_and_barcode() -> None:
    """Test ProductCategory compatibility and Barcode verification."""
    category = _sample_category()
    assert category.is_compatible_with_condition(StorageCondition(15.0, 30.0))
    category.update_storage_condition(StorageCondition(0.0, 5.0))
    assert category.default_condition.max_temp_c == 5.0
    with pytest.raises(InvalidDataError):
        ProductCategory("", "General", StorageCondition())

    barcode = Barcode("4810001234567", "EAN13")
    assert barcode.verify_checksum()
    assert "[EAN13]" in barcode.format_label()
    with pytest.raises(InvalidDataError):
        Barcode("123", "UNKNOWN")


def test_product_and_subclasses() -> None:
    """Test Product, PerishableProduct, FragileProduct, and HazardousProduct."""
    cat = _sample_category()
    bc = Barcode("123456", "EAN13")

    product = Product("SKU-1", "Box", cat, bc, 2.0, 0.1, 100.0)
    assert product.calculate_total_weight(3) == 6.0
    assert product.calculate_total_value(3) == 300.0
    assert product.apply_discount(10.0) == 90.0
    with pytest.raises(InvalidDataError):
        product.calculate_total_weight(-1)
    with pytest.raises(InvalidDataError):
        product.calculate_total_value(-1)
    with pytest.raises(InvalidDataError):
        product.apply_discount(150.0)
    with pytest.raises(InvalidDataError):
        Product("", "Box", cat, bc, 1.0, 0.1, 10.0)

    milk = PerishableProduct("SKU-M", "Milk", cat, bc, 1.0, 0.05, 5.0, shelf_life_days=10)
    assert not milk.is_expired(date(2026, 1, 1), date(2026, 1, 5))
    assert milk.needs_priority_dispatch(date(2026, 1, 1), date(2026, 1, 8))
    assert milk.is_expired(date(2026, 1, 1), date(2026, 1, 20))
    with pytest.raises(InvalidDataError):
        PerishableProduct("SKU-M", "Milk", cat, bc, 1.0, 0.05, 5.0, shelf_life_days=0)

    glass = FragileProduct("SKU-G", "Glass", cat, bc, 1.0, 0.1, 20.0, max_stack_layers=3)
    assert glass.can_stack(2)
    assert not glass.can_stack(5)
    assert glass.calculate_packaging_volume(2) == 0.23
    with pytest.raises(InvalidDataError):
        glass.calculate_packaging_volume(-1)
    with pytest.raises(InvalidDataError):
        FragileProduct("SKU-G", "Glass", cat, bc, 1.0, 0.1, 20.0, max_stack_layers=0)

    chem = HazardousProduct("SKU-H", "Acid", cat, bc, 5.0, 0.2, 50.0, 3, "UN1203")
    assert chem.requires_isolation_zone()
    assert "UN1203" in chem.format_safety_label()
    with pytest.raises(InvalidDataError):
        HazardousProduct("SKU-H", "Acid", cat, bc, 5.0, 0.2, 50.0, 12, "UN1203")


def test_batch_pallet_and_stock_record() -> None:
    """Test InventoryBatch, Pallet loading/wrapping, and StockRecord reservations."""
    product = Product("SKU-1", "Item", _sample_category(), Barcode("12345", "EAN13"), 10.0, 0.2, 50.0)
    batch = InventoryBatch("BAT-1", product, 5, expiry_date=date(2026, 12, 31))
    batch.deduct_quantity(2, date(2026, 6, 1))
    assert batch.quantity == 3
    with pytest.raises(ExpiredProductError):
        batch.deduct_quantity(1, date(2027, 1, 1))
    batch.place_in_quarantine()
    with pytest.raises(InsufficientStockError):
        batch.deduct_quantity(1, date(2026, 6, 1))
    with pytest.raises(InvalidDataError):
        InventoryBatch("", product, 5)

    pallet = Pallet("PAL-1", max_weight_kg=50.0)
    with pytest.raises(InvalidDataError):
        pallet.wrap_for_shipping()
    pallet.load_batch(batch)
    assert pallet.calculate_current_weight() == 30.0
    pallet.wrap_for_shipping()
    assert pallet.is_wrapped
    with pytest.raises(BinCapacityExceededError):
        pallet.load_batch(InventoryBatch("BAT-2", product, 5))
    with pytest.raises(InvalidDataError):
        Pallet("", 50.0)

    record = StockRecord(product, StorageBin("B-01"), available_quantity=12)
    record.reserve(5)
    assert record.available_quantity == 7
    assert record.is_low_stock()
    record.release_reservation(2)
    assert record.reserved_quantity == 3
    with pytest.raises(InsufficientStockError):
        record.reserve(50)
    with pytest.raises(InvalidDataError):
        record.release_reservation(50)
    with pytest.raises(InvalidDataError):
        StockRecord(product, StorageBin("B-01"), available_quantity=-1)