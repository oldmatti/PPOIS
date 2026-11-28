"""Quality inspection record model."""

from constants import STATUS_COMPLETED, STATUS_CREATED, STATUS_FAILED
from exceptions import InvalidDataError, QualityCheckFailedError
from .inventory_batch import InventoryBatch
from .quality_inspector import QualityInspector


class QualityCheck:
    """Tracks a formal quality inspection performed on an inventory batch."""

    def __init__(
        self,
        check_id: str,
        batch: InventoryBatch,
        inspector: QualityInspector,
    ) -> None:
        if not check_id:
            raise InvalidDataError("Quality check ID is required.")
        self.check_id = check_id
        self.batch = batch
        self.inspector = inspector
        self.status = STATUS_CREATED
        self.defect_rate_percent = 0.0

    def execute_check(self, defect_rate_percent: float) -> bool:
        """Run the inspection via the assigned inspector and record the outcome."""
        if not 0.0 <= defect_rate_percent <= 100.0:
            raise InvalidDataError("Defect rate must be between 0 and 100 percent.")
        self.defect_rate_percent = defect_rate_percent
        try:
            self.inspector.inspect_batch(self.batch, defect_rate_percent)
        except QualityCheckFailedError:
            self.status = STATUS_FAILED
            raise
        self.status = STATUS_COMPLETED
        return True