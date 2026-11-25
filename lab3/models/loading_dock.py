"""Loading dock model for inbound and outbound vehicles."""

from typing import Optional

from exceptions import DockOccupiedError, InvalidDataError


class LoadingDock:
    """Represents a truck bay used for loading and unloading goods."""

    def __init__(self, dock_number: str, dock_type: str) -> None:
        if not dock_number or dock_type not in ("inbound", "outbound", "universal"):
            raise InvalidDataError("Invalid dock number or dock type.")
        self.dock_number = dock_number
        self.dock_type = dock_type
        self.current_vehicle_plate: Optional[str] = None
        self.is_operational = True

    def assign_vehicle(self, vehicle_plate: str) -> None:
        """Assign a vehicle to the dock if it is free and operational."""
        if not self.is_operational:
            raise DockOccupiedError(f"Dock {self.dock_number} is out of service.")
        if self.current_vehicle_plate is not None:
            raise DockOccupiedError(f"Dock {self.dock_number} is already occupied.")
        self.current_vehicle_plate = vehicle_plate

    def release_vehicle(self) -> Optional[str]:
        """Clear the dock and return the departed vehicle plate."""
        departed = self.current_vehicle_plate
        self.current_vehicle_plate = None
        return departed

    def set_maintenance_mode(self, enabled: bool) -> None:
        """Toggle maintenance mode when the dock is empty."""
        if enabled and self.current_vehicle_plate is not None:
            raise DockOccupiedError("Cannot close an occupied dock for maintenance.")
        self.is_operational = not enabled