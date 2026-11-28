"""Barcode model for product identification."""

from exceptions import InvalidDataError


class Barcode:
    """Represents a product barcode in a supported encoding format."""

    VALID_FORMATS = ("EAN13", "UPC", "CODE128")

    def __init__(self, code: str, barcode_format: str = "EAN13") -> None:
        if not code or barcode_format not in self.VALID_FORMATS:
            raise InvalidDataError("Invalid barcode value or unsupported format.")
        self.code = code
        self.barcode_format = barcode_format
        self.is_verified = False

    def verify_checksum(self) -> bool:
        """Validate barcode structure and mark it as verified if valid."""
        is_valid = self.code.isdigit() if self.barcode_format in ("EAN13", "UPC") else self.code.isalnum()
        self.is_verified = is_valid
        return is_valid

    def format_label(self) -> str:
        """Return a printable label string with format and code."""
        return f"[{self.barcode_format}] {self.code}"