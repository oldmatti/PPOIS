from datetime import date


class Person:
    """Base class representing a person with general demographic data."""

    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date):
        self.person_id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def calculate_age(self, current_date: date = None) -> int:
        """Calculates and returns the person's exact age in years."""
        if current_date is None:
            current_date = date.today()

        return current_date.year - self.birth_date.year - (
                (current_date.month, current_date.day) < (self.birth_date.month, self.birth_date.day)
        )