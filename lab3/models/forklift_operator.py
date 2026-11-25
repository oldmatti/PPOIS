"""Forklift operator model with license validation."""

from exceptions import InvalidDataError, UnauthorizedAccessError
from .access_badge import AccessBadge
from .employee import Employee


class ForkliftOperator(Employee):
    """Certified operator authorized to drive warehouse forklifts."""

    def __init__(
        self,
        employee_id: str,
        full_name: str,
        hourly_rate: float,
        badge: AccessBadge,
        license_number: str,
    ) -> None:
        super().__init__(employee_id, full_name, "forklift_operator", hourly_rate, badge)
        if not license_number:
            raise InvalidDataError("Forklift operator must have a license number.")
        self.license_number = license_number
        self.license_valid = True
        self.pallets_moved = 0

    def record_pallet_move(self) -> None:
        """Increment moved pallet counter if the operator license is valid."""
        if not self.license_valid:
            raise UnauthorizedAccessError(f"Operator {self.employee_id} license is suspended.")
        self.pallets_moved += 1

    def suspend_license(self) -> None:
        """Revoke operating privileges due to safety violation or expiry."""
        self.license_valid = False