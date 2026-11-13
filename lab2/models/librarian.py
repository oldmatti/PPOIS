from datetime import date
from .employee import Employee
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .library import Library

class Librarian(Employee):
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, salary: float, position: str, library: 'Library'):
        super().__init__(person_id, first_name, last_name, birth_date, salary, position)
        self.library = library