"""Warehouse manager model with approval authority."""

from typing import List

from exceptions import UnauthorizedAccessError
from .access_badge import AccessBadge
from .employee import Employee


class WarehouseManager(Employee):
    """Supervisor managing warehouse teams and approving expenses."""

    def __init__(
        self,
        employee_id: str,
        full_name: str,
        hourly_rate: float,
        badge: AccessBadge,
        approval_limit: float,
    ) -> None:
        super().__init__(employee_id, full_name, "manager", hourly_rate, badge)
        self.approval_limit = approval_limit
        self.subordinates: List[Employee] = []

    def add_subordinate(self, employee: Employee) -> None:
        """Assign an employee under this manager's supervision."""
        if employee not in self.subordinates:
            self.subordinates.append(employee)

    def approve_expense(self, amount: float) -> bool:
        """Approve an operational expense within the manager's limit."""
        if amount > self.approval_limit:
            raise UnauthorizedAccessError(
                f"Expense {amount} exceeds manager limit {self.approval_limit}."
            )
        return True

    def calculate_team_payroll(self) -> float:
        """Sum accumulated pay across all supervised employees."""
        return round(sum(emp.calculate_pay() for emp in self.subordinates), 2)