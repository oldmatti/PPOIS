"""Warehouse shelf model containing storage bins."""

from typing import List, Optional

from exceptions import InvalidDataError
from .storage_bin import StorageBin


class Shelf:
    """Represents a horizontal shelf level inside a rack."""

    def __init__(self, shelf_id: str, level: int, max_bins: int) -> None:
        if not shelf_id or level < 1 or max_bins < 1:
            raise InvalidDataError("Shelf requires a valid ID, positive level, and capacity.")
        self.shelf_id = shelf_id
        self.level = level
        self.max_bins = max_bins
        self.bins: List[StorageBin] = []

    def add_bin(self, storage_bin: StorageBin) -> None:
        """Attach a storage bin to the shelf if capacity allows."""
        if len(self.bins) >= self.max_bins:
            raise InvalidDataError(f"Shelf {self.shelf_id} has reached maximum bin count.")
        self.bins.append(storage_bin)

    def find_bin_with_sku(self, sku: str) -> Optional[StorageBin]:
        """Locate the first bin on this shelf containing the given SKU."""
        for storage_bin in self.bins:
            if sku in storage_bin.items:
                return storage_bin
        return None

    def calculate_total_weight(self) -> float:
        """Compute the combined weight of all bins on the shelf."""
        return sum(storage_bin.current_weight_kg for storage_bin in self.bins)