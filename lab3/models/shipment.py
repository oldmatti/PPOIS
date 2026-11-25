"""Outbound shipment model linking orders, pallets, and carriers."""

from typing import List

from constants import STATUS_COMPLETED, STATUS_CREATED, STATUS_IN_PROGRESS
from exceptions import InvalidDataError, InvalidOrderStateError
from .carrier import Carrier
from .outbound_order import OutboundOrder
from .pallet import Pallet


class Shipment:
    """Represents a dispatched consignment handed over to a carrier."""

    def __init__(
        self,
        shipment_id: str,
        order: OutboundOrder,
        carrier: Carrier,
    ) -> None:
        if not shipment_id:
            raise InvalidDataError("Shipment ID is required.")
        self.shipment_id = shipment_id
        self.order = order
        self.carrier = carrier
        self.pallets: List[Pallet] = []
        self.status = STATUS_CREATED

    def attach_pallet(self, pallet: Pallet) -> None:
        """Attach a wrapped pallet to the shipment before dispatch."""
        if self.status != STATUS_CREATED or not pallet.is_wrapped:
            raise InvalidOrderStateError("Only wrapped pallets can be added to a new shipment.")
        self.pallets.append(pallet)

    def dispatch(self) -> float:
        """Dispatch the shipment with the carrier and return delivery cost."""
        if self.status != STATUS_CREATED or not self.pallets:
            raise InvalidOrderStateError("Shipment must be created and contain pallets.")
        total_weight = sum(pallet.calculate_current_weight() for pallet in self.pallets)
        if not self.carrier.can_carry(total_weight):
            raise InvalidDataError("Carrier cannot transport the total shipment weight.")
        self.status = STATUS_IN_PROGRESS
        return self.carrier.calculate_shipping_cost(total_weight)

    def mark_delivered(self) -> None:
        """Mark an in-transit shipment as delivered."""
        if self.status != STATUS_IN_PROGRESS:
            raise InvalidOrderStateError("Only an in-progress shipment can be delivered.")
        self.status = STATUS_COMPLETED