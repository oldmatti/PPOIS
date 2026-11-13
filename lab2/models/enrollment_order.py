from datetime import date
from typing import TYPE_CHECKING
from .order import Order

if TYPE_CHECKING:
    from .student import Student

class EnrollmentOrder(Order):
    """Specific order for enrolling a new student."""

    def __init__(self, document_id: str, creation_date: date, student: 'Student'):
        super().__init__(document_id, creation_date, f"Enrollment of {student.last_name}", "Enrollment")
        self.student = student