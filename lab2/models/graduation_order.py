from datetime import date
from typing import TYPE_CHECKING
from .order import Order
if TYPE_CHECKING:
    from .student import Student

class GraduationOrder(Order):
    def __init__(self, document_id: str, creation_date: date, student: 'Student', degree: str):
        super().__init__(document_id, creation_date, f"Graduation of {student.last_name}", "Graduation")
        self.student = student
        self.degree = degree