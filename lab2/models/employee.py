from datetime import date
from .person import Person


class Employee(Person):
    """Class representing a university employee. Inherits from Person."""

    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, salary: float, position: str):
        super().__init__(person_id, first_name, last_name, birth_date)

        self.salary = salary
        self.position = position
        self.department = None

    def assign_department(self, department):
        """Assigns the employee to a specific department."""
        self.department = department