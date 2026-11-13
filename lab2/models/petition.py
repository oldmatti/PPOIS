from datetime import date
from typing import TYPE_CHECKING
from .document import Document

if TYPE_CHECKING:
    from .student import Student

class Petition(Document):
    """Class representing a student's petition or formal request."""

    def __init__(self, document_id: str, creation_date: date, title: str, student: 'Student'):
        super().__init__(document_id, creation_date, title)
        self.student = student
        self.is_approved = False  # одобрено ли заявление деканом

    def approve(self):
        """Approves the student's petition."""
        self.is_approved = True