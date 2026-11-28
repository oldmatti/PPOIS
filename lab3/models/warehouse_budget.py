"""Warehouse budget model controlling operational expenses."""

from typing import List

from exceptions import BudgetExceededError, InvalidDataError


class WarehouseBudget:
    """Tracks allocated warehouse funds and enforces spending limits."""

    def __init__(self, fiscal_year: int, total_limit: float) -> None:
        if fiscal_year < 2000 or total_limit < 0:
            raise InvalidDataError("Valid fiscal year and non-negative budget are required.")
        self.fiscal_year = fiscal_year
        self.total_limit = total_limit
        self.spent_amount = 0.0
        self.expense_log: List[str] = []

    def allocate_expense(self, description: str, amount: float) -> float:
        """Deduct an expense from the budget if sufficient funds remain."""
        if not description or amount <= 0:
            raise InvalidDataError("Expense requires a description and positive amount.")
        if self.spent_amount + amount > self.total_limit:
            raise BudgetExceededError(f"Expense '{description}' exceeds remaining budget.")
        self.spent_amount = round(self.spent_amount + amount, 2)
        self.expense_log.append(f"{description}: {amount}")
        return self.get_remaining_budget()

    def get_remaining_budget(self) -> float:
        """Return the unspent portion of the budget."""
        return round(self.total_limit - self.spent_amount, 2)