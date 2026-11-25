"""Climate sensor model monitoring a storage zone."""

from constants import DEFAULT_TARGET_TEMP_C
from exceptions import EquipmentUnavailableError
from .storage_zone import StorageZone
from .warehouse_equipment import WarehouseEquipment


class TemperatureSensor(WarehouseEquipment):
    """Measures temperature inside a storage zone and reports violations."""

    def __init__(
        self,
        equipment_id: str,
        model_name: str,
        zone: StorageZone,
        last_reading_c: float = DEFAULT_TARGET_TEMP_C,
    ) -> None:
        super().__init__(equipment_id, model_name)
        self.zone = zone
        self.last_reading_c = last_reading_c

    def record_reading(self, measured_temp_c: float) -> None:
        """Store a new reading and propagate it to the monitored zone."""
        if not self.is_operational:
            raise EquipmentUnavailableError(f"Sensor {self.equipment_id} is offline.")
        self.last_reading_c = measured_temp_c
        self.zone.update_temperature(measured_temp_c)

    def calibrate(self, offset_c: float) -> float:
        """Adjust the latest temperature reading by a calibration offset."""
        self.last_reading_c = round(self.last_reading_c + offset_c, 2)
        return self.last_reading_c