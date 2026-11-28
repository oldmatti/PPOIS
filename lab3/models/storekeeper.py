"""Storekeeper model responsible for bin placement and picking."""

from typing import List

from .access_badge import AccessBadge
from .employee import Employee
from .storage_bin import StorageBin


class Storekeeper(Employee):
    """Warehouse worker handling stock placement and order picking."""

    def __init__(
        self,
        employee_id: str,
        full_name: str,
        hourly_rate: float,
        badge: AccessBadge,
        assigned_zone_code: str,
    ) -> None:
        super().__init__(employee_id, full_name, "storekeeper", hourly_rate, badge)
        self.assigned_zone_code = assigned_zone_code
        self.completed_picks: List[str] = []

    def place_in_bin(
        self,
        storage_bin: StorageBin,
        sku: str,
        quantity: int,
        weight_kg: float,
        volume_m3: float,
    ) -> None:
        """Place received items into a target storage bin."""
        storage_bin.add_item(sku, quantity, weight_kg, volume_m3)

    def record_completed_pick(self, task_id: str) -> None:
        """Log a completed picking task for performance tracking."""
        self.completed_picks.append(task_id)