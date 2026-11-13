from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .student import Student
from exceptions.scholarship_denied_exception import ScholarshipDeniedException

class Scholarship:
    def __init__(self, name: str, amount: float, min_gpa: float):
        self.name = name
        self.amount = amount
        self.min_gpa = min_gpa

    def check_eligibility(self, student: 'Student') -> bool:
        if student.gradebook and student.gradebook.calculate_gpa() < self.min_gpa:
            raise ScholarshipDeniedException(student.last_name, "Low GPA")
        return True