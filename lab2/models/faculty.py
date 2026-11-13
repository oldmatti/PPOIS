from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .department import Department

class Faculty:
    """Class representing a university faculty (a collection of departments)."""

    def __init__(self, faculty_id: str, name: str):
        self.faculty_id = faculty_id
        self.name = name
        self.departments: List['Department'] = []

    def add_department(self, department: 'Department'):
        """Adds a department to the faculty's structure."""
        self.departments.append(department)