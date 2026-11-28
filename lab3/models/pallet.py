"""Warehouse pallet model for grouping inventory batches."""

from typing import List

from constants import DEFAULT_PALLET_MAX_WEIGHT_KG
from exceptions import BinCapacityExceededError, InvalidDataError
from .inventory_batch import InventoryBatch


class Pallet:
    """Represents a transport pallet loaded with inventory batches."""

    def __init__(
        self,
        pallet_id: str,
        max_weight_kg: float = DEFAULT_PALLET_MAX_WEIGHT_KG,
    ) -> None:
        if not pallet_id or max_weight_kg <= 0:
            raise InvalidDataError("Pallet ID and positive max weight are required.")
        self.pallet_id = pallet_id
        self.max_weight_kg = max_weight_kg
        self.batches: List[InventoryBatch] = []
        self.is_wrapped = False

    def calculate_current_weight(self) -> float:
        """Calculate total weight of all batches currently on the pallet."""
        return round(
            sum(batch.product.calculate_total_weight(batch.quantity) for batch in self.batches),
            3,
        )

    def load_batch(self, batch: InventoryBatch) -> None:
        """Add a batch to the pallet if weight limit is not exceeded."""
        batch_weight = batch.product.calculate_total_weight(batch.quantity)
        if self.calculate_current_weight() + batch_weight > self.max_weight_kg:
            raise BinCapacityExceededError(f"Pallet {self.pallet_id} weight limit exceeded.")
        self.batches.append(batch)

    def wrap_for_shipping(self) -> None:
        """Mark the pallet as stretch-wrapped if it contains at least one batch."""
        if not self.batches:
            raise InvalidDataError("Cannot wrap an empty pallet.")
        self.is_wrapped = True