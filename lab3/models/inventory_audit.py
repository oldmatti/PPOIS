"""Inventory audit model for reconciling expected and actual bin stock."""

from typing import Dict

from constants import STATUS_COMPLETED, STATUS_CREATED
from exceptions import InvalidDataError
from .storage_bin import StorageBin


class InventoryAudit:
    """Compares system stock counts against physical counts in a bin."""

    def __init__(self, audit_id: str, target_bin: StorageBin, auditor_id: str) -> None:
        if not audit_id or not auditor_id:
            raise InvalidDataError("Audit ID and auditor ID are required.")
        self.audit_id = audit_id
        self.target_bin = target_bin
        self.auditor_id = auditor_id
        self.discrepancies: Dict[str, int] = {}
        self.status = STATUS_CREATED

    def run_audit(self, counted_items: Dict[str, int]) -> Dict[str, int]:
        """Compare physical counts against bin records and store differences."""
        all_skus = set(self.target_bin.items.keys()) | set(counted_items.keys())
        self.discrepancies.clear()
        for sku in all_skus:
            expected = self.target_bin.items.get(sku, 0)
            actual = counted_items.get(sku, 0)
            if actual != expected:
                self.discrepancies[sku] = actual - expected
        self.status = STATUS_COMPLETED
        return self.discrepancies

    def has_discrepancies(self) -> bool:
        """Return True if any SKU showed a count mismatch."""
        return len(self.discrepancies) > 0