"""Individual storage bin model."""

from typing import Dict

from constants import DEFAULT_BIN_MAX_VOLUME_M3, DEFAULT_BIN_MAX_WEIGHT_KG
from exceptions import BinCapacityExceededError, InsufficientStockError, InvalidDataError


class StorageBin:
    """Represents a single storage cell on a shelf."""

    def __init__(
        self,
        bin_code: str,
        max_weight_kg: float = DEFAULT_BIN_MAX_WEIGHT_KG,
        max_volume_m3: float = DEFAULT_BIN_MAX_VOLUME_M3,
    ) -> None:
        if not bin_code or max_weight_kg <= 0 or max_volume_m3 <= 0:
            raise InvalidDataError("Bin code and positive capacity limits are required.")
        self.bin_code = bin_code
        self.max_weight_kg = max_weight_kg
        self.max_volume_m3 = max_volume_m3
        self.current_weight_kg = 0.0
        self.current_volume_m3 = 0.0
        self.items: Dict[str, int] = {}

    def add_item(self, sku: str, quantity: int, weight_kg: float, volume_m3: float) -> None:
        """Place items into the bin while enforcing weight and volume limits."""
        if quantity <= 0 or weight_kg < 0 or volume_m3 < 0:
            raise InvalidDataError("Quantity must be positive and metrics non-negative.")
        if self.current_weight_kg + weight_kg > self.max_weight_kg:
            raise BinCapacityExceededError(f"Weight limit exceeded in bin {self.bin_code}.")
        if self.current_volume_m3 + volume_m3 > self.max_volume_m3:
            raise BinCapacityExceededError(f"Volume limit exceeded in bin {self.bin_code}.")
        self.items[sku] = self.items.get(sku, 0) + quantity
        self.current_weight_kg += weight_kg
        self.current_volume_m3 += volume_m3

    def remove_item(self, sku: str, quantity: int, weight_kg: float, volume_m3: float) -> None:
        """Remove items from the bin and update occupied weight and volume."""
        available = self.items.get(sku, 0)
        if quantity <= 0 or available < quantity:
            raise InsufficientStockError(f"Not enough {sku} in bin {self.bin_code}.")
        self.items[sku] = available - quantity
        if self.items[sku] == 0:
            del self.items[sku]
        self.current_weight_kg = max(0.0, self.current_weight_kg - weight_kg)
        self.current_volume_m3 = max(0.0, self.current_volume_m3 - volume_m3)

    def calculate_fill_ratio(self) -> float:
        """Return the highest utilization ratio between weight and volume."""
        weight_ratio = self.current_weight_kg / self.max_weight_kg
        volume_ratio = self.current_volume_m3 / self.max_volume_m3
        return round(max(weight_ratio, volume_ratio), 3)