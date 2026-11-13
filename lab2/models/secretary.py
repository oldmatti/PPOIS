from datetime import date
from .employee import Employee


class Secretary(Employee):
    """Class representing a secretary who manages paperwork and documents."""

    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date,
                 salary: float, position: str, typing_speed: int):
        super().__init__(person_id, first_name, last_name, birth_date, salary, position)
        self.typing_speed = typing_speed  # скорость печати (символов в минуту)