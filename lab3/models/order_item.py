"""Order line item linking a product and requested quantity."""

from constants import MIN_ORDER_QUANTITY
from exceptions import InvalidDataError
from .product import Product


class OrderItem:
    """Represents a single product line inside an inbound or outbound order."""

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity < MIN_ORDER_QUANTITY:
            raise InvalidDataError(f"Order item quantity must be at least {MIN_ORDER_QUANTITY}.")
        self.product = product
        self.quantity = quantity

    def calculate_line_total(self) -> float:
        """Compute total monetary value of this order line."""
        return self.product.calculate_total_value(self.quantity)

    def calculate_line_weight(self) -> float:
        """Compute total weight of this order line in kilograms."""
        return self.product.calculate_total_weight(self.quantity)