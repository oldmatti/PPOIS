"""Client model for outbound order recipients."""

from exceptions import InvalidDataError
from .address import Address


class Client:
    """Represents a customer ordering goods from the warehouse."""

    def __init__(
        self,
        client_id: str,
        company_name: str,
        shipping_address: Address,
        credit_limit: float,
    ) -> None:
        if not client_id or not company_name or credit_limit < 0:
            raise InvalidDataError("Client requires ID, name, and non-negative credit limit.")
        self.client_id = client_id
        self.company_name = company_name
        self.shipping_address = shipping_address
        self.credit_limit = credit_limit
        self.current_balance = 0.0

    def can_place_order(self, order_amount: float) -> bool:
        """Check whether the client has enough remaining credit for an order."""
        return self.current_balance + order_amount <= self.credit_limit

    def add_charge(self, amount: float) -> float:
        """Increase the client's outstanding balance."""
        if amount < 0:
            raise InvalidDataError("Charge amount cannot be negative.")
        self.current_balance = round(self.current_balance + amount, 2)
        return self.current_balance