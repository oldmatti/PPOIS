"""Warehouse rack model composed of shelves."""

from typing import List, Optional

from exceptions import InvalidDataError
from .shelf import Shelf
from .storage_bin import StorageBin


class Rack:
    """Represents a vertical storage rack holding multiple shelves."""

    def __init__(self, rack_code: str, aisle: str, max_shelves: int) -> None:
        if not rack_code or not aisle or max_shelves < 1:
            raise InvalidDataError("Rack requires code, aisle, and positive shelf limit.")
        self.rack_code = rack_code
        self.aisle = aisle
        self.max_shelves = max_shelves
        self.shelves: List[Shelf] = []

    def add_shelf(self, shelf: Shelf) -> None:
        """Register a shelf inside the rack."""
        if len(self.shelves) >= self.max_shelves:
            raise InvalidDataError(f"Rack {self.rack_code} cannot hold more shelves.")
        self.shelves.append(shelf)

    def find_available_bin(self, required_weight_kg: float) -> Optional[StorageBin]:
        """Find a bin in the rack that can accommodate the requested weight."""
        for shelf in self.shelves:
            for storage_bin in shelf.bins:
                free_weight = storage_bin.max_weight_kg - storage_bin.current_weight_kg
                if free_weight >= required_weight_kg:
                    return storage_bin
        return None

    def calculate_total_load(self) -> float:
        """Return total weight stored across all shelves in the rack."""
        return sum(shelf.calculate_total_weight() for shelf in self.shelves)