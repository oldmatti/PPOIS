from datetime import date
from typing import TYPE_CHECKING, List
from .employee import Employee

if TYPE_CHECKING:
    from .subject import Subject
    from .student import Student


class Professor(Employee):
    """Class representing a university professor. Inherits from Employee."""

    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, salary: float, position: str,
                 degree: str):
        super().__init__(person_id, first_name, last_name, birth_date, salary, position)
        self.degree = degree
        self.subjects: List['Subject'] = []

    def add_subject(self, subject: 'Subject'):
        """Adds a subject to the professor's teaching list."""
        self.subjects.append(subject)

    def exam_student(self, student: 'Student', subject: 'Subject', grade_value: int, exam_date: date):
        """Evaluates a student and adds a new grade to their gradebook."""
        from .grade import Grade

        new_grade = Grade(grade_value, exam_date, subject, self)

        if student.gradebook:
            student.gradebook.add_grade(new_grade)