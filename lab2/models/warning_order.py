from datetime import date
from typing import TYPE_CHECKING
from .order import Order
if TYPE_CHECKING:
    from .student import Student

class WarningOrder(Order):
    def __init__(self, document_id: str, creation_date: date, student: 'Student', reason: str):
        super().__init__(document_id, creation_date, f"Warning for {student.last_name}", "Warning")
        self.student = student
        self.reason = reason