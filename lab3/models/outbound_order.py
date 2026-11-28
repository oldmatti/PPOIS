"""Outbound customer order model for shipping stock."""

from typing import List

from constants import STATUS_CANCELLED, STATUS_COMPLETED, STATUS_CREATED, STATUS_IN_PROGRESS
from exceptions import InvalidDataError, InvalidOrderStateError
from .order_item import OrderItem


class OutboundOrder:
    """Represents a customer order scheduled for picking and dispatch."""

    def __init__(self, order_id: str, client_id: str, priority: int = 1) -> None:
        if not order_id or not client_id or not 1 <= priority <= 5:
            raise InvalidDataError("Outbound order requires ID, client ID, and priority 1-5.")
        self.order_id = order_id
        self.client_id = client_id
        self.priority = priority
        self.items: List[OrderItem] = []
        self.status = STATUS_CREATED

    def add_item(self, item: OrderItem) -> None:
        """Append an item line while the order is in created state."""
        if self.status != STATUS_CREATED:
            raise InvalidOrderStateError("Cannot add items once fulfillment has started.")
        self.items.append(item)

    def start_fulfillment(self) -> None:
        """Move the order to in-progress for warehouse picking."""
        if self.status != STATUS_CREATED or not self.items:
            raise InvalidOrderStateError("Order must be created and contain items.")
        self.status = STATUS_IN_PROGRESS

    def mark_shipped(self) -> None:
        """Mark an in-progress outbound order as shipped."""
        if self.status != STATUS_IN_PROGRESS:
            raise InvalidOrderStateError("Only an in-progress order can be shipped.")
        self.status = STATUS_COMPLETED

    def cancel_order(self) -> None:
        """Cancel the outbound order if it has not been shipped."""
        if self.status == STATUS_COMPLETED:
            raise InvalidOrderStateError("Shipped order cannot be cancelled.")
        self.status = STATUS_CANCELLED

    def calculate_total_weight(self) -> float:
        """Compute combined weight of all order items."""
        return round(sum(item.calculate_line_weight() for item in self.items), 3)