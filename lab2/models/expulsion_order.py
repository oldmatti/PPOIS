from datetime import date
from typing import TYPE_CHECKING
from .order import Order

if TYPE_CHECKING:
    from .student import Student

class ExpulsionOrder(Order):
    """Specific order for expelling a student."""

    def __init__(self, document_id: str, creation_date: date, student: 'Student', reason: str):
        super().__init__(document_id, creation_date, f"Expulsion of {student.last_name}", "Expulsion")
        self.student = student
        self.reason = reason  # причина отчисления (например, "Академическая задолженность")