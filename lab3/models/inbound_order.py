"""Inbound purchase order model for receiving stock."""

from typing import List

from constants import STATUS_CANCELLED, STATUS_COMPLETED, STATUS_CREATED, STATUS_IN_PROGRESS
from exceptions import InvalidDataError, InvalidOrderStateError
from .order_item import OrderItem


class InboundOrder:
    """Represents an incoming delivery of goods from a supplier."""

    def __init__(self, order_id: str, supplier_id: str) -> None:
        if not order_id or not supplier_id:
            raise InvalidDataError("Inbound order requires order ID and supplier ID.")
        self.order_id = order_id
        self.supplier_id = supplier_id
        self.items: List[OrderItem] = []
        self.status = STATUS_CREATED

    def add_item(self, item: OrderItem) -> None:
        """Add a product line while the order is still in created state."""
        if self.status != STATUS_CREATED:
            raise InvalidOrderStateError("Cannot modify items after receiving has started.")
        self.items.append(item)

    def start_receiving(self) -> None:
        """Transition the order into the active receiving phase."""
        if self.status != STATUS_CREATED or not self.items:
            raise InvalidOrderStateError("Order must be created and non-empty to start receiving.")
        self.status = STATUS_IN_PROGRESS

    def complete_receiving(self) -> None:
        """Mark the inbound order as fully received."""
        if self.status != STATUS_IN_PROGRESS:
            raise InvalidOrderStateError("Only an in-progress order can be completed.")
        self.status = STATUS_COMPLETED

    def cancel_order(self) -> None:
        """Cancel an inbound order before completion."""
        if self.status == STATUS_COMPLETED:
            raise InvalidOrderStateError("Completed inbound order cannot be cancelled.")
        self.status = STATUS_CANCELLED

    def calculate_total_cost(self) -> float:
        """Return total cost of all items in the inbound order."""
        return round(sum(item.calculate_line_total() for item in self.items), 2)