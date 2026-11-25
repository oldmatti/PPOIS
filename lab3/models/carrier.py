"""Logistics carrier model for transporting shipments."""

from exceptions import InvalidDataError


class Carrier:
    """Represents a transport company delivering outbound shipments."""

    def __init__(
        self,
        carrier_id: str,
        name: str,
        rate_per_kg: float,
        max_vehicle_load_kg: float,
    ) -> None:
        if not carrier_id or not name or rate_per_kg <= 0 or max_vehicle_load_kg <= 0:
            raise InvalidDataError("Carrier requires valid ID, name, and positive rates.")
        self.carrier_id = carrier_id
        self.name = name
        self.rate_per_kg = rate_per_kg
        self.max_vehicle_load_kg = max_vehicle_load_kg
        self.is_active = True

    def calculate_shipping_cost(self, weight_kg: float) -> float:
        """Compute delivery cost based on shipment weight."""
        if weight_kg < 0:
            raise InvalidDataError("Shipment weight cannot be negative.")
        return round(weight_kg * self.rate_per_kg, 2)

    def can_carry(self, weight_kg: float) -> bool:
        """Check if an active carrier can transport the requested load."""
        return self.is_active and 0 < weight_kg <= self.max_vehicle_load_kg