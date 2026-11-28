"""Automated conveyor belt model for moving packages."""

from exceptions import EquipmentOverloadError, EquipmentUnavailableError, InvalidDataError
from .warehouse_equipment import WarehouseEquipment


class ConveyorBelt(WarehouseEquipment):
    """Represents a motorized conveyor line between warehouse zones."""

    def __init__(
        self,
        equipment_id: str,
        model_name: str,
        max_weight_kg: float,
        max_speed_mps: float,
    ) -> None:
        super().__init__(equipment_id, model_name)
        if max_weight_kg <= 0 or max_speed_mps <= 0:
            raise InvalidDataError("Conveyor requires positive weight and speed limits.")
        self.max_weight_kg = max_weight_kg
        self.max_speed_mps = max_speed_mps
        self.current_speed_mps = 0.0

    def start_belt(self, speed_mps: float) -> None:
        """Start the conveyor at a valid operating speed."""
        if not self.is_operational:
            raise EquipmentUnavailableError(f"Conveyor {self.equipment_id} is out of service.")
        if not 0 < speed_mps <= self.max_speed_mps:
            raise InvalidDataError("Requested speed is out of conveyor limits.")
        self.current_speed_mps = speed_mps

    def stop_belt(self) -> None:
        """Halt the conveyor belt."""
        self.current_speed_mps = 0.0

    def transport_load(self, weight_kg: float) -> bool:
        """Validate load weight on a running conveyor belt."""
        if self.current_speed_mps <= 0:
            raise EquipmentUnavailableError("Conveyor belt must be running to move loads.")
        if weight_kg > self.max_weight_kg:
            raise EquipmentOverloadError(f"Load {weight_kg}kg exceeds conveyor capacity.")
        return True