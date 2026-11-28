"""Industrial weighing scale model for pallets and packages."""

from exceptions import EquipmentOverloadError, EquipmentUnavailableError, InvalidDataError
from .pallet import Pallet
from .warehouse_equipment import WarehouseEquipment


class WeighingScale(WarehouseEquipment):
    """Measures pallet weights and checks against scale capacity."""

    def __init__(
        self,
        equipment_id: str,
        model_name: str,
        max_capacity_kg: float,
    ) -> None:
        super().__init__(equipment_id, model_name)
        if max_capacity_kg <= 0:
            raise InvalidDataError("Scale maximum capacity must be positive.")
        self.max_capacity_kg = max_capacity_kg
        self.last_weight_kg = 0.0

    def weigh_pallet(self, pallet: Pallet) -> float:
        """Weigh a pallet and raise an error if it overloads the scale."""
        if not self.is_operational:
            raise EquipmentUnavailableError(f"Scale {self.equipment_id} is unavailable.")
        weight = pallet.calculate_current_weight()
        if weight > self.max_capacity_kg:
            raise EquipmentOverloadError(f"Pallet weight {weight}kg exceeds scale limit.")
        self.last_weight_kg = weight
        return weight

    def reset_tare(self) -> None:
        """Reset the last measured weight back to zero."""
        self.last_weight_kg = 0.0