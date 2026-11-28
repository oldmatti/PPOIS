"""Fragile product model with stacking and shock constraints."""

from exceptions import InvalidDataError
from .barcode import Barcode
from .product import Product
from .product_category import ProductCategory


class FragileProduct(Product):
    """Represents a delicate product requiring special handling."""

    def __init__(
        self,
        sku: str,
        name: str,
        category: ProductCategory,
        barcode: Barcode,
        weight_kg: float,
        volume_m3: float,
        unit_price: float,
        max_stack_layers: int,
        requires_padding: bool = True,
    ) -> None:
        super().__init__(sku, name, category, barcode, weight_kg, volume_m3, unit_price)
        if max_stack_layers < 1:
            raise InvalidDataError("Maximum stack layers must be at least 1.")
        self.max_stack_layers = max_stack_layers
        self.requires_padding = requires_padding

    def can_stack(self, target_layers: int) -> bool:
        """Verify whether the requested number of stacked layers is safe."""
        return 1 <= target_layers <= self.max_stack_layers

    def calculate_packaging_volume(self, quantity: int, padding_factor: float = 1.15) -> float:
        """Estimate total volume including protective padding."""
        if quantity < 0 or padding_factor < 1.0:
            raise InvalidDataError("Invalid quantity or padding factor.")
        multiplier = padding_factor if self.requires_padding else 1.0
        return round(self.volume_m3 * quantity * multiplier, 3)