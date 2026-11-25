"""Base warehouse employee model."""

from exceptions import InvalidDataError, UnauthorizedAccessError
from .access_badge import AccessBadge


class Employee:
    """Represents a warehouse staff member with a role and access badge."""

    def __init__(
        self,
        employee_id: str,
        full_name: str,
        role: str,
        hourly_rate: float,
        badge: AccessBadge,
    ) -> None:
        if not employee_id or not full_name or not role or hourly_rate <= 0:
            raise InvalidDataError("Employee requires valid ID, name, role, and positive rate.")
        self.employee_id = employee_id
        self.full_name = full_name
        self.role = role
        self.hourly_rate = hourly_rate
        self.badge = badge
        self.hours_worked = 0.0

    def log_work_hours(self, hours: float) -> None:
        """Record worked hours for payroll calculation."""
        if hours <= 0:
            raise InvalidDataError("Logged hours must be positive.")
        self.hours_worked += hours

    def calculate_pay(self) -> float:
        """Compute total pay based on logged hours and hourly rate."""
        return round(self.hours_worked * self.hourly_rate, 2)

    def verify_clearance(self, required_level: int) -> bool:
        """Ensure the employee badge is active and meets the required level."""
        if not self.badge.is_active or self.badge.clearance_level < required_level:
            raise UnauthorizedAccessError(f"Employee {self.employee_id} lacks clearance.")
        return True