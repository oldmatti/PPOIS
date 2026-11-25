"""Warehouse picking task model."""

from constants import STATUS_COMPLETED, STATUS_CREATED, STATUS_IN_PROGRESS
from exceptions import InvalidDataError, InvalidOrderStateError
from .outbound_order import OutboundOrder
from .storage_bin import StorageBin
from .storekeeper import Storekeeper


class PickingTask:
    """Represents a task for a storekeeper to pick items for an order."""

    def __init__(
        self,
        task_id: str,
        order: OutboundOrder,
        source_bin: StorageBin,
        assignee: Storekeeper,
    ) -> None:
        if not task_id:
            raise InvalidDataError("Picking task ID is required.")
        self.task_id = task_id
        self.order = order
        self.source_bin = source_bin
        self.assignee = assignee
        self.status = STATUS_CREATED

    def start_picking(self) -> None:
        """Begin execution of the picking task."""
        if self.status != STATUS_CREATED:
            raise InvalidOrderStateError("Picking task has already started or finished.")
        self.status = STATUS_IN_PROGRESS

    def complete_picking(self, sku: str, quantity: int, weight_kg: float, volume_m3: float) -> None:
        """Remove picked stock from the bin and log completion on the storekeeper."""
        if self.status != STATUS_IN_PROGRESS:
            raise InvalidOrderStateError("Picking task must be in progress to complete.")
        self.source_bin.remove_item(sku, quantity, weight_kg, volume_m3)
        self.assignee.record_completed_pick(self.task_id)
        self.status = STATUS_COMPLETED