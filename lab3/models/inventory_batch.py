"""Inventory batch model tracking a specific lot of products."""

from datetime import date
from typing import Optional

from exceptions import ExpiredProductError, InsufficientStockError, InvalidDataError
from .product import Product


class InventoryBatch:
    """Represents a tracked batch of a single product with expiry monitoring."""

    def __init__(
        self,
        batch_id: str,
        product: Product,
        quantity: int,
        expiry_date: Optional[date] = None,
    ) -> None:
        if not batch_id or quantity < 0:
            raise InvalidDataError("Batch ID is required and quantity cannot be negative.")
        self.batch_id = batch_id
        self.product = product
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.is_quarantined = False

    def is_expired(self, current_date: date) -> bool:
        """Check whether the batch has passed its expiration date."""
        if self.expiry_date is None:
            return False
        return current_date > self.expiry_date

    def deduct_quantity(self, amount: int, current_date: date) -> None:
        """Deduct units from the batch after checking expiry and availability."""
        if self.is_expired(current_date):
            raise ExpiredProductError(f"Batch {self.batch_id} is expired.")
        if self.is_quarantined or amount <= 0 or amount > self.quantity:
            raise InsufficientStockError(f"Cannot deduct {amount} from batch {self.batch_id}.")
        self.quantity -= amount

    def place_in_quarantine(self) -> None:
        """Block the batch from being picked or shipped."""
        self.is_quarantined = True