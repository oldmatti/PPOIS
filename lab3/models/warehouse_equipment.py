"""Base model for all warehouse equipment and machinery."""

from typing import List

from exceptions import EquipmentUnavailableError, InvalidDataError
from .maintenance_record import MaintenanceRecord


class WarehouseEquipment:
    """Represents a piece of physical equipment used in warehouse operations."""

    def __init__(self, equipment_id: str, model_name: str) -> None:
        if not equipment_id or not model_name:
            raise InvalidDataError("Equipment ID and model name are required.")
        self.equipment_id = equipment_id
        self.model_name = model_name
        self.is_operational = True
        self.is_in_use = False
        self.maintenance_history: List[MaintenanceRecord] = []

    def checkout(self) -> None:
        """Reserve equipment for active use if operational and free."""
        if not self.is_operational or self.is_in_use:
            raise EquipmentUnavailableError(f"Equipment {self.equipment_id} is unavailable.")
        self.is_in_use = True

    def release(self) -> None:
        """Return equipment to the available pool."""
        self.is_in_use = False

    def log_maintenance(self, record: MaintenanceRecord) -> None:
        """Record a malfunction and take equipment offline until repaired."""
        self.maintenance_history.append(record)
        self.is_operational = False
        self.is_in_use = False

    def restore_to_service(self) -> None:
        """Mark equipment as operational after maintenance."""
        self.is_operational = True