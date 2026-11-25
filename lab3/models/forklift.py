"""Electric forklift model for moving pallets."""

from constants import (
    DEFAULT_FORKLIFT_BATTERY_MAX_PERCENT,
    DEFAULT_FORKLIFT_BATTERY_MIN_PERCENT,
    DEFAULT_FORKLIFT_MAX_LOAD_KG,
)
from exceptions import EquipmentOverloadError, EquipmentUnavailableError, InvalidDataError
from .pallet import Pallet
from .warehouse_equipment import WarehouseEquipment


class Forklift(WarehouseEquipment):
    """Represents a battery-powered forklift with load and charge limits."""

    def __init__(
        self,
        equipment_id: str,
        model_name: str,
        max_load_kg: float = DEFAULT_FORKLIFT_MAX_LOAD_KG,
        battery_percent: float = DEFAULT_FORKLIFT_BATTERY_MAX_PERCENT,
    ) -> None:
        super().__init__(equipment_id, model_name)
        if max_load_kg <= 0 or not 0 <= battery_percent <= DEFAULT_FORKLIFT_BATTERY_MAX_PERCENT:
            raise InvalidDataError("Forklift requires positive load limit and valid battery.")
        self.max_load_kg = max_load_kg
        self.battery_percent = battery_percent

    def lift_pallet(self, pallet: Pallet, battery_cost: float = 5.0) -> None:
        """Lift a pallet after checking operational status, battery, and weight."""
        if not self.is_operational or self.battery_percent < DEFAULT_FORKLIFT_BATTERY_MIN_PERCENT:
            raise EquipmentUnavailableError(f"Forklift {self.equipment_id} cannot operate.")
        pallet_weight = pallet.calculate_current_weight()
        if pallet_weight > self.max_load_kg:
            raise EquipmentOverloadError(f"Pallet exceeds forklift {self.equipment_id} capacity.")
        self.battery_percent = max(0.0, self.battery_percent - battery_cost)

    def charge_battery(self, amount: float) -> float:
        """Recharge the forklift battery up to the maximum percentage."""
        if amount <= 0:
            raise InvalidDataError("Charge amount must be positive.")
        self.battery_percent = min(
            DEFAULT_FORKLIFT_BATTERY_MAX_PERCENT,
            self.battery_percent + amount,
        )
        return self.battery_percent