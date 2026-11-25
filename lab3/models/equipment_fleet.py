"""Fleet manager model overseeing all warehouse equipment."""

from typing import List, Optional, Type

from exceptions import InvalidDataError
from .warehouse_equipment import WarehouseEquipment


class EquipmentFleet:
    """Maintains the registry of all machinery and tracks maintenance costs."""

    def __init__(self, warehouse_id: str) -> None:
        if not warehouse_id:
            raise InvalidDataError("Warehouse ID is required for equipment fleet.")
        self.warehouse_id = warehouse_id
        self.equipment_list: List[WarehouseEquipment] = []

    def register_equipment(self, equipment: WarehouseEquipment) -> None:
        """Add a new piece of equipment to the warehouse fleet."""
        self.equipment_list.append(equipment)

    def find_available_by_type(
        self,
        equipment_cls: Type[WarehouseEquipment],
    ) -> Optional[WarehouseEquipment]:
        """Locate the first operational and free unit of the requested class."""
        for item in self.equipment_list:
            if isinstance(item, equipment_cls) and item.is_operational and not item.is_in_use:
                return item
        return None

    def calculate_total_maintenance_cost(self) -> float:
        """Sum all maintenance expenses across the entire fleet."""
        total = 0.0
        for item in self.equipment_list:
            total += sum(record.cost for record in item.maintenance_history)
        return round(total, 2)