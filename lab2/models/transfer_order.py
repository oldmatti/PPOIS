from datetime import date
from typing import TYPE_CHECKING
from .order import Order
if TYPE_CHECKING:
    from .student import Student
    from .study_group import StudyGroup

class TransferOrder(Order):
    def __init__(self, document_id: str, creation_date: date, student: 'Student', new_group: 'StudyGroup'):
        super().__init__(document_id, creation_date, f"Transfer {student.last_name}", "Transfer")
        self.student = student
        self.new_group = new_group