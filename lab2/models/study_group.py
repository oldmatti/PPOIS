from typing import TYPE_CHECKING, List
from .subgroup import Subgroup

if TYPE_CHECKING:
    from .student import Student


class StudyGroup:
    """Class representing a university study group."""

    def __init__(self, group_name: str):
        self.group_name = group_name
        self.students: List['Student'] = []
        self.subgroups: List[Subgroup] = []

    def add_student(self, student: 'Student'):
        """Adds a student to the group and establishes a two-way link."""
        self.students.append(student)
        student.assign_group(self)

    def split_into_subgroups(self):
        """Splits the group's students equally into two subgroups."""

        self.subgroups = [Subgroup(1, self), Subgroup(2, self)]

        mid = len(self.students) // 2

        # распределение студентов с помощью срезов
        for s in self.students[:mid]:
            self.subgroups[0].add_student(s)

        for s in self.students[mid:]:
            self.subgroups[1].add_student(s)