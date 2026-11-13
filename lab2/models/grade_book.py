from typing import TYPE_CHECKING, List
from .grade import Grade

if TYPE_CHECKING:
    from .student import Student


class GradeBook:
    """Class representing a student's grade book, storing the history of grades."""

    def __init__(self, book_id: str, student: 'Student'):
        self.book_id = book_id
        self.student = student
        self.grades: List[Grade] = []  # пустой список для оценок

    def add_grade(self, grade: Grade):
        """Mutator: adds a new grade to the grade book."""
        self.grades.append(grade)

    def calculate_average_score(self) -> float:
        """Analytical method: calculates and returns the Grade Point Average (GPA)."""
        if not self.grades:
            return 0.0

        total = sum(g.value for g in self.grades)
        return total / len(self.grades)

    def has_debts(self) -> bool:
        """Checks if the student has any academic debts (grades below 4 on a 10-point scale)."""
        for g in self.grades:
            if g.value < 4:
                return True
        return False