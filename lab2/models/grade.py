from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .professor import Professor
    from .subject import Subject

class Grade:
    """Class representing a single student grade for an exam or assignment."""

    def __init__(self, value: int, grade_date: date, subject: 'Subject', professor: 'Professor'):
        self.value = value
        self.grade_date = grade_date
        self.subject = subject
        self.professor = professor