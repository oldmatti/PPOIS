from datetime import date
from typing import TYPE_CHECKING
from .employee import Employee

if TYPE_CHECKING:
    from .faculty import Faculty


class Dean(Employee):
    """Class representing a faculty dean. Inherits from Employee."""

    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date,
                 salary: float, position: str, faculty: 'Faculty'):
        super().__init__(person_id, first_name, last_name, birth_date, salary, position)
        self.faculty = faculty  # Факультет, которым управляет декан