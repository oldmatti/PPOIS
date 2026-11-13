from .deanery_exception import DeaneryException

class InsufficientCreditsException(DeaneryException):
    def __init__(self, student_name: str):
        super().__init__(f"Student {student_name} does not have enough credits or completed subjects to transfer.")