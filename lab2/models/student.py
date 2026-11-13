from datetime import date
from typing import TYPE_CHECKING
from .person import Person

if TYPE_CHECKING:
    from .study_group import StudyGroup
    from .grade_book import GradeBook


class Student(Person):
    """Class representing a university student. Inherits from Person."""

    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date):
        super().__init__(person_id, first_name, last_name, birth_date)

        self.study_group: 'StudyGroup' = None
        self.gradebook: 'GradeBook' = None

    def assign_group(self, group: 'StudyGroup'):
        """Assigns the student to a specific study group."""
        self.study_group = group