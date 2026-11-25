"""Warehouse storage zone model with climate control."""

from typing import List

from constants import DEFAULT_TARGET_TEMP_C
from exceptions import InvalidDataError, TemperatureViolationError
from .rack import Rack
from .storage_condition import StorageCondition


class StorageZone:
    """Represents a logical warehouse zone with defined storage conditions."""

    def __init__(
        self,
        zone_code: str,
        name: str,
        condition: StorageCondition,
        current_temp_c: float = DEFAULT_TARGET_TEMP_C,
    ) -> None:
        if not zone_code or not name:
            raise InvalidDataError("Zone code and name are required.")
        self.zone_code = zone_code
        self.name = name
        self.condition = condition
        self.current_temp_c = current_temp_c
        self.racks: List[Rack] = []

    def add_rack(self, rack: Rack) -> None:
        """Add a rack to this storage zone."""
        self.racks.append(rack)

    def update_temperature(self, new_temp_c: float) -> None:
        """Update the zone temperature and verify compliance with conditions."""
        self.current_temp_c = new_temp_c
        if not self.condition.is_temperature_acceptable(new_temp_c):
            raise TemperatureViolationError(
                f"Zone {self.zone_code} temperature {new_temp_c}C is out of range."
            )

    def count_total_bins(self) -> int:
        """Count all storage bins across all racks in the zone."""
        total = 0
        for rack in self.racks:
            total += sum(len(shelf.bins) for shelf in rack.shelves)
        return total