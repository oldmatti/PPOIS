"""Staff scheduler model assigning employees to shifts."""

from typing import Dict, List

from exceptions import InvalidDataError
from .employee import Employee
from .shift import Shift


class StaffScheduler:
    """Manages shift assignments and prevents duplicate bookings."""

    def __init__(self, warehouse_id: str) -> None:
        if not warehouse_id:
            raise InvalidDataError("Warehouse ID is required for scheduler.")
        self.warehouse_id = warehouse_id
        self.assignments: Dict[str, List[Employee]] = {}

    def assign_employee_to_shift(self, shift: Shift, employee: Employee) -> None:
        """Assign an employee to an open shift."""
        if shift.is_closed:
            raise InvalidDataError(f"Shift {shift.shift_id} is already closed.")
        shift_staff = self.assignments.setdefault(shift.shift_id, [])
        if employee in shift_staff:
            raise InvalidDataError(f"Employee {employee.employee_id} is already on this shift.")
        shift_staff.append(employee)

    def get_shift_headcount(self, shift_id: str) -> int:
        """Return the number of employees assigned to a specific shift."""
        return len(self.assignments.get(shift_id, []))