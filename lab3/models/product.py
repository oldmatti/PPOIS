"""Base warehouse product model."""

from exceptions import InvalidDataError
from .barcode import Barcode
from .product_category import ProductCategory


class Product:
    """Represents a catalog product stored in the warehouse."""

    def __init__(
        self,
        sku: str,
        name: str,
        category: ProductCategory,
        barcode: Barcode,
        weight_kg: float,
        volume_m3: float,
        unit_price: float,
    ) -> None:
        if not sku or not name or weight_kg <= 0 or volume_m3 <= 0 or unit_price < 0:
            raise InvalidDataError("Product requires valid SKU, name, and positive dimensions.")
        self.sku = sku
        self.name = name
        self.category = category
        self.barcode = barcode
        self.weight_kg = weight_kg
        self.volume_m3 = volume_m3
        self.unit_price = unit_price

    def calculate_total_weight(self, quantity: int) -> float:
        """Calculate combined weight for a given number of units."""
        if quantity < 0:
            raise InvalidDataError("Quantity cannot be negative.")
        return round(self.weight_kg * quantity, 3)

    def calculate_total_value(self, quantity: int) -> float:
        """Calculate monetary value for a given number of units."""
        if quantity < 0:
            raise InvalidDataError("Quantity cannot be negative.")
        return round(self.unit_price * quantity, 2)

    def apply_discount(self, percent: float) -> float:
        """Reduce unit price by the specified percentage."""
        if not 0 <= percent <= 100:
            raise InvalidDataError("Discount percentage must be between 0 and 100.")
        self.unit_price = round(self.unit_price * (1 - percent / 100), 2)
        return self.unit_price