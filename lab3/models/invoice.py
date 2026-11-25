"""Financial invoice model for billing clients."""

from constants import DEFAULT_TAX_RATE
from exceptions import InvalidDataError
from .client import Client
from .outbound_order import OutboundOrder


class Invoice:
    """Represents a billing document generated for a client's outbound order."""

    def __init__(
        self,
        invoice_id: str,
        client: Client,
        order: OutboundOrder,
        tax_rate: float = DEFAULT_TAX_RATE,
    ) -> None:
        if not invoice_id or not 0.0 <= tax_rate <= 1.0:
            raise InvalidDataError("Invoice requires valid ID and tax rate between 0 and 1.")
        self.invoice_id = invoice_id
        self.client = client
        self.order = order
        self.tax_rate = tax_rate
        self.is_paid = False

    def calculate_subtotal(self) -> float:
        """Calculate pre-tax order total across all items."""
        return round(sum(item.calculate_line_total() for item in self.order.items), 2)

    def calculate_total_with_tax(self) -> float:
        """Compute the final invoice amount including tax."""
        subtotal = self.calculate_subtotal()
        return round(subtotal * (1 + self.tax_rate), 2)

    def mark_as_paid(self) -> None:
        """Record the invoice as settled."""
        self.is_paid = True