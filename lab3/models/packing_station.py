"""Packing station model for preparing outbound pallets."""

from typing import List

from exceptions import InvalidDataError
from .pallet import Pallet


class PackingStation:
    """Represents a workstation where picked goods are packed and wrapped."""

    def __init__(self, station_id: str, max_daily_pallets: int) -> None:
        if not station_id or max_daily_pallets < 1:
            raise InvalidDataError("Station ID and positive daily capacity are required.")
        self.station_id = station_id
        self.max_daily_pallets = max_daily_pallets
        self.packed_pallets: List[Pallet] = []
        self.is_active = True

    def pack_pallet(self, pallet: Pallet) -> None:
        """Wrap a loaded pallet and record it at the station."""
        if not self.is_active or len(self.packed_pallets) >= self.max_daily_pallets:
            raise InvalidDataError(f"Packing station {self.station_id} cannot process more pallets.")
        pallet.wrap_for_shipping()
        self.packed_pallets.append(pallet)

    def reset_daily_counter(self) -> int:
        """Clear packed pallets for the next shift and return the previous count."""
        processed = len(self.packed_pallets)
        self.packed_pallets.clear()
        return processed