"""Handheld barcode scanner model."""

from typing import List

from exceptions import EquipmentUnavailableError
from .barcode import Barcode
from .warehouse_equipment import WarehouseEquipment


class BarcodeScanner(WarehouseEquipment):
    """Scans and verifies product barcodes during warehouse workflows."""

    def __init__(self, equipment_id: str, model_name: str) -> None:
        super().__init__(equipment_id, model_name)
        self.scanned_codes: List[str] = []

    def scan_barcode(self, barcode: Barcode) -> bool:
        """Scan a barcode, verify its checksum, and store it in history."""
        if not self.is_operational:
            raise EquipmentUnavailableError(f"Scanner {self.equipment_id} is offline.")
        is_valid = barcode.verify_checksum()
        if is_valid:
            self.scanned_codes.append(barcode.code)
        return is_valid

    def clear_scan_history(self) -> int:
        """Clear stored scan history and return the number of removed entries."""
        count = len(self.scanned_codes)
        self.scanned_codes.clear()
        return count