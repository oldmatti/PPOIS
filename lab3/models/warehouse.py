"""Top-level physical warehouse model."""

from typing import List, Optional

from exceptions import InvalidDataError
from .address import Address
from .loading_dock import LoadingDock
from .security_checkpoint import SecurityCheckpoint
from .storage_zone import StorageZone


class Warehouse:
    """Aggregates zones, loading docks, and security checkpoints."""

    def __init__(self, warehouse_id: str, name: str, address: Address) -> None:
        if not warehouse_id or not name:
            raise InvalidDataError("Warehouse ID and name are required.")
        self.warehouse_id = warehouse_id
        self.name = name
        self.address = address
        self.zones: List[StorageZone] = []
        self.docks: List[LoadingDock] = []
        self.checkpoints: List[SecurityCheckpoint] = []

    def add_zone(self, zone: StorageZone) -> None:
        """Register a storage zone inside the warehouse."""
        self.zones.append(zone)

    def add_dock(self, dock: LoadingDock) -> None:
        """Register a loading dock at the warehouse."""
        self.docks.append(dock)

    def find_free_dock(self, dock_type: str) -> Optional[LoadingDock]:
        """Return the first available operational dock matching the requested type."""
        for dock in self.docks:
            matches = dock.dock_type in (dock_type, "universal")
            if matches and dock.is_operational and dock.current_vehicle_plate is None:
                return dock
        return None

    def get_total_bin_count(self) -> int:
        """Calculate the total number of storage bins across all zones."""
        return sum(zone.count_total_bins() for zone in self.zones)