"""Customer return request model."""

from constants import STATUS_CANCELLED, STATUS_COMPLETED, STATUS_CREATED
from exceptions import InvalidDataError, InvalidOrderStateError
from .outbound_order import OutboundOrder


class ReturnRequest:
    """Represents a client request to return items from an outbound order."""

    def __init__(
        self,
        request_id: str,
        order: OutboundOrder,
        sku: str,
        quantity: int,
        reason: str,
    ) -> None:
        if not request_id or not sku or quantity <= 0 or not reason:
            raise InvalidDataError("Return request requires valid ID, SKU, quantity, and reason.")
        self.request_id = request_id
        self.order = order
        self.sku = sku
        self.quantity = quantity
        self.reason = reason
        self.status = STATUS_CREATED

    def approve_return(self) -> None:
        """Approve a pending return request."""
        if self.status != STATUS_CREATED:
            raise InvalidOrderStateError("Only a newly created return request can be approved.")
        self.status = STATUS_COMPLETED

    def reject_return(self) -> None:
        """Reject a pending return request."""
        if self.status != STATUS_CREATED:
            raise InvalidOrderStateError("Only a newly created return request can be rejected.")
        self.status = STATUS_CANCELLED