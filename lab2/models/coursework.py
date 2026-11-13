from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .student import Student
    from .professor import Professor

class Coursework:
    def __init__(self, title: str, student: 'Student', advisor: 'Professor'):
        self.title = title
        self.student = student
        self.advisor = advisor
        self.grade = 0