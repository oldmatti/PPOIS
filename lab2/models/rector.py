from datetime import date
from .employee import Employee

class Rector(Employee):
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, salary: float, position: str, degree: str):
        super().__init__(person_id, first_name, last_name, birth_date, salary, position)
        self.degree = degree