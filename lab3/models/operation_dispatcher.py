"""Central dispatcher managing inbound and outbound warehouse orders."""

from typing import Dict

from constants import STATUS_COMPLETED
from exceptions import OrderNotFoundError
from .inbound_order import InboundOrder
from .outbound_order import OutboundOrder


class OperationDispatcher:
    """Tracks active orders and provides lookup and status statistics."""

    def __init__(self, dispatcher_id: str) -> None:
        self.dispatcher_id = dispatcher_id
        self.inbound_orders: Dict[str, InboundOrder] = {}
        self.outbound_orders: Dict[str, OutboundOrder] = {}

    def register_inbound_order(self, order: InboundOrder) -> None:
        """Store an inbound order in the dispatcher registry."""
        self.inbound_orders[order.order_id] = order

    def register_outbound_order(self, order: OutboundOrder) -> None:
        """Store an outbound order in the dispatcher registry."""
        self.outbound_orders[order.order_id] = order

    def get_outbound_order(self, order_id: str) -> OutboundOrder:
        """Retrieve an outbound order by ID or raise OrderNotFoundError."""
        if order_id not in self.outbound_orders:
            raise OrderNotFoundError(f"Outbound order {order_id} not found.")
        return self.outbound_orders[order_id]

    def count_pending_outbound(self) -> int:
        """Count outbound orders that have not yet reached completed status."""
        return sum(
            1 for order in self.outbound_orders.values() if order.status != STATUS_COMPLETED
        )