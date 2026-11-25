"""Hazardous product model with safety classification."""

from exceptions import InvalidDataError
from .barcode import Barcode
from .product import Product
from .product_category import ProductCategory


class HazardousProduct(Product):
    """Represents a dangerous material requiring isolation and clearance."""

    def __init__(
        self,
        sku: str,
        name: str,
        category: ProductCategory,
        barcode: Barcode,
        weight_kg: float,
        volume_m3: float,
        unit_price: float,
        hazard_class: int,
        un_number: str,
    ) -> None:
        super().__init__(sku, name, category, barcode, weight_kg, volume_m3, unit_price)
        if not 1 <= hazard_class <= 9 or not un_number:
            raise InvalidDataError("Hazard class must be 1-9 and UN number is required.")
        self.hazard_class = hazard_class
        self.un_number = un_number

    def requires_isolation_zone(self) -> bool:
        """Return True for high-risk hazard classes requiring isolated storage."""
        return self.hazard_class in (1, 2, 3, 6, 7)

    def format_safety_label(self) -> str:
        """Generate a standardized hazard warning label."""
        return f"HAZARD CLASS {self.hazard_class} | {self.un_number} | {self.sku}"