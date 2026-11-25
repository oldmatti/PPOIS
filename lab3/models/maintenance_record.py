"""Maintenance log record for warehouse equipment."""

from exceptions import InvalidDataError


class MaintenanceRecord:
    """Tracks a single repair or scheduled maintenance event."""

    def __init__(
        self,
        record_id: str,
        equipment_id: str,
        description: str,
        cost: float,
    ) -> None:
        if not record_id or not equipment_id or not description or cost < 0:
            raise InvalidDataError("Maintenance record requires valid IDs, description, and cost.")
        self.record_id = record_id
        self.equipment_id = equipment_id
        self.description = description
        self.cost = cost
        self.is_completed = False

    def complete_maintenance(self) -> None:
        """Mark the maintenance work as finished."""
        self.is_completed = True

    def is_major_repair(self, cost_threshold: float) -> bool:
        """Determine whether the repair cost exceeds a given threshold."""
        if cost_threshold < 0:
            raise InvalidDataError("Cost threshold cannot be negative.")
        return self.cost >= cost_threshold