from .deanery_exception import DeaneryException

class RetakeLimitExceededException(DeaneryException):
    def __init__(self, student_name: str, subject_name: str):
        super().__init__(f"Student {student_name} has exceeded the retake limit (more than 3 times) for subject '{subject_name}'.")