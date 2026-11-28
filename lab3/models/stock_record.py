"""Stock ledger record linking a product to a storage bin."""

from constants import DEFAULT_LOW_STOCK_THRESHOLD
from exceptions import InsufficientStockError, InvalidDataError
from .product import Product
from .storage_bin import StorageBin


class StockRecord:
    """Tracks available and reserved stock for a product in a specific bin."""

    def __init__(
        self,
        product: Product,
        storage_bin: StorageBin,
        available_quantity: int = 0,
        reserved_quantity: int = 0,
    ) -> None:
        if available_quantity < 0 or reserved_quantity < 0:
            raise InvalidDataError("Stock quantities cannot be negative.")
        self.product = product
        self.storage_bin = storage_bin
        self.available_quantity = available_quantity
        self.reserved_quantity = reserved_quantity

    def reserve(self, amount: int) -> None:
        """Move units from available stock to reserved stock."""
        if amount <= 0 or amount > self.available_quantity:
            raise InsufficientStockError(f"Cannot reserve {amount} of {self.product.sku}.")
        self.available_quantity -= amount
        self.reserved_quantity += amount

    def release_reservation(self, amount: int) -> None:
        """Return reserved units back to available stock."""
        if amount <= 0 or amount > self.reserved_quantity:
            raise InvalidDataError("Invalid reservation release amount.")
        self.reserved_quantity -= amount
        self.available_quantity += amount

    def is_low_stock(self, threshold: int = DEFAULT_LOW_STOCK_THRESHOLD) -> bool:
        """Check whether available quantity has dropped below the reorder threshold."""
        return self.available_quantity <= threshold