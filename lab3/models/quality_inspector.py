"""Quality inspector model for incoming and outgoing batch checks."""

from exceptions import QualityCheckFailedError
from .access_badge import AccessBadge
from .employee import Employee
from .inventory_batch import InventoryBatch


class QualityInspector(Employee):
    """Specialist verifying product condition and quarantining defects."""

    def __init__(
        self,
        employee_id: str,
        full_name: str,
        hourly_rate: float,
        badge: AccessBadge,
        certification_code: str,
    ) -> None:
        super().__init__(employee_id, full_name, "quality_inspector", hourly_rate, badge)
        self.certification_code = certification_code
        self.inspections_completed = 0

    def inspect_batch(self, batch: InventoryBatch, defect_rate_percent: float) -> bool:
        """Approve a batch or quarantine it if defect rate exceeds 5%."""
        self.inspections_completed += 1
        if defect_rate_percent > 5.0:
            batch.place_in_quarantine()
            raise QualityCheckFailedError(f"Batch {batch.batch_id} failed quality check.")
        return True