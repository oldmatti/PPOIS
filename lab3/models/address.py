"""Physical address model for warehouse locations."""

from exceptions import InvalidDataError


class Address:
    """Represents a physical street address."""

    def __init__(
        self,
        country: str,
        city: str,
        street: str,
        building: str,
        postal_code: str,
    ) -> None:
        if not country or not city or not street:
            raise InvalidDataError("Country, city, and street are required.")
        self.country = country
        self.city = city
        self.street = street
        self.building = building
        self.postal_code = postal_code

    def format_full_address(self) -> str:
        """Return a formatted single-line postal address."""
        parts = [self.postal_code, self.country, self.city, self.street, self.building]
        return ", ".join(part for part in parts if part)

    def is_same_city(self, other: "Address") -> bool:
        """Check whether another address is located in the same city."""
        return self.city.lower() == other.city.lower()

    def validate_postal_code(self) -> bool:
        """Verify that the postal code contains only alphanumeric characters."""
        cleaned = self.postal_code.replace("-", "").replace(" ", "")
        return cleaned.isalnum()