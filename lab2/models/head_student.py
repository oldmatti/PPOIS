from datetime import date
from .student import Student


class HeadStudent(Student):
    """Class representing a head student (Starosta) of a study group. Inherits from Student."""

    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, scholarship_bonus: float):
        super().__init__(person_id, first_name, last_name, birth_date)
        self.scholarship_bonus = scholarship_bonus  # надбавка к стипендии за обязанности старосты