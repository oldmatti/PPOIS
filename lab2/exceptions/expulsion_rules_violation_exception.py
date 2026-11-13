from .deanery_exception import DeaneryException

class ExpulsionRulesViolationException(DeaneryException):
    def __init__(self, student_name: str):
        super().__init__(f"Expulsion rules violation: cannot expel {student_name} without a valid reason or dean's signature.")