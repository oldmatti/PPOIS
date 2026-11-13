from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .student import Student
    from .study_group import StudyGroup

class Subgroup:
    """Class representing a subgroup within a main study group."""

    def __init__(self, subgroup_number: int, parent_group: 'StudyGroup'):
        self.subgroup_number = subgroup_number
        self.parent_group = parent_group
        self.students: List['Student'] = []  # список студентов в подгруппе

    def add_student(self, student: 'Student'):
        """Adds a student to this specific subgroup."""
        self.students.append(student)