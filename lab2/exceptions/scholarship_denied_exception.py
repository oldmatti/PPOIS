from .deanery_exception import DeaneryException

class ScholarshipDeniedException(DeaneryException):
    def __init__(self, student_name: str, reason: str):
        super().__init__(f"Scholarship denied for {student_name}. Reason: {reason}.")