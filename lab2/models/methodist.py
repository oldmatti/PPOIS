from datetime import date
from .employee import Employee
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .curriculum import Curriculum

class Methodist(Employee):
    def __init__(self, person_id: int, first_name: str, last_name: str, birth_date: date, salary: float, position: str):
        super().__init__(person_id, first_name, last_name, birth_date, salary, position)

    def develop_curriculum(self, major: str) -> 'Curriculum':
        from .curriculum import Curriculum
        return Curriculum(f"CUR-{major[:3]}", major)