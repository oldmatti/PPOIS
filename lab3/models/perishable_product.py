"""Perishable product model with shelf-life tracking."""

from datetime import date

from constants import DEFAULT_EXPIRY_WARNING_DAYS
from exceptions import InvalidDataError
from .barcode import Barcode
from .product import Product
from .product_category import ProductCategory


class PerishableProduct(Product):
    """Represents a product with a limited shelf life."""

    def __init__(
        self,
        sku: str,
        name: str,
        category: ProductCategory,
        barcode: Barcode,
        weight_kg: float,
        volume_m3: float,
        unit_price: float,
        shelf_life_days: int,
    ) -> None:
        super().__init__(sku, name, category, barcode, weight_kg, volume_m3, unit_price)
        if shelf_life_days <= 0:
            raise InvalidDataError("Shelf life must be a positive number of days.")
        self.shelf_life_days = shelf_life_days

    def is_expired(self, production_date: date, current_date: date) -> bool:
        """Determine whether the product has passed its shelf life."""
        elapsed_days = (current_date - production_date).days
        return elapsed_days > self.shelf_life_days

    def needs_priority_dispatch(self, production_date: date, current_date: date) -> bool:
        """Check if remaining shelf life is within the warning threshold."""
        remaining_days = self.shelf_life_days - (current_date - production_date).days
        return 0 <= remaining_days <= DEFAULT_EXPIRY_WARNING_DAYS