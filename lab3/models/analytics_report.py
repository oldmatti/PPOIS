"""Warehouse analytics report model summarizing key KPIs."""

from exceptions import InvalidDataError
from .operation_dispatcher import OperationDispatcher
from .warehouse import Warehouse
from .warehouse_budget import WarehouseBudget


class AnalyticsReport:
    """Generates operational and financial summaries for a warehouse."""

    def __init__(
        self,
        report_id: str,
        warehouse: Warehouse,
        dispatcher: OperationDispatcher,
        budget: WarehouseBudget,
    ) -> None:
        if not report_id:
            raise InvalidDataError("Report ID is required.")
        self.report_id = report_id
        self.warehouse = warehouse
        self.dispatcher = dispatcher
        self.budget = budget

    def generate_summary(self) -> str:
        """Build a multi-line operational summary string."""
        total_bins = self.warehouse.get_total_bin_count()
        pending_orders = self.dispatcher.count_pending_outbound()
        remaining = self.budget.get_remaining_budget()
        return (
            f"Report {self.report_id} | Warehouse: {self.warehouse.name}\n"
            f"Zones: {len(self.warehouse.zones)}, Bins: {total_bins}\n"
            f"Pending outbound orders: {pending_orders}\n"
            f"Remaining budget: {remaining}"
        )

    def calculate_budget_utilization_percent(self) -> float:
        """Return the percentage of the annual budget already spent."""
        if self.budget.total_limit == 0:
            return 0.0
        return round((self.budget.spent_amount / self.budget.total_limit) * 100, 2)