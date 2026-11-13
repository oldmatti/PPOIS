from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .student import Student

class Contract:
    def __init__(self, contract_id: str, student: 'Student', amount: float):
        self.contract_id = contract_id
        self.student = student
        self.amount = amount
        self.is_active = False

    def sign_contract(self):
        self.is_active = True