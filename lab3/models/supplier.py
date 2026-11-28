"""Supplier model for inbound product deliveries."""

from typing import List

from exceptions import InvalidDataError


class Supplier:
    """Represents an external vendor supplying goods to the warehouse."""

    def __init__(
        self,
        supplier_id: str,
        company_name: str,
        contact_email: str,
        reliability_score: float = 100.0,
    ) -> None:
        if not supplier_id or not company_name or "@" not in contact_email:
            raise InvalidDataError("Supplier requires ID, company name, and valid email.")
        if not 0.0 <= reliability_score <= 100.0:
            raise InvalidDataError("Reliability score must be between 0 and 100.")
        self.supplier_id = supplier_id
        self.company_name = company_name
        self.contact_email = contact_email
        self.reliability_score = reliability_score
        self.supplied_skus: List[str] = []

    def register_sku(self, sku: str) -> None:
        """Associate a product SKU with this supplier."""
        if sku and sku not in self.supplied_skus:
            self.supplied_skus.append(sku)

    def adjust_reliability(self, delta: float) -> float:
        """Update supplier reliability score within the 0-100 range."""
        updated = max(0.0, min(100.0, self.reliability_score + delta))
        self.reliability_score = round(updated, 2)
        return self.reliability_score