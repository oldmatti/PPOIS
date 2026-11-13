from .deanery_exception import DeaneryException

class StudentNotFoundException(DeaneryException):
    def __init__(self, student_id: int):
        super().__init__(f"Student with ID {student_id} not found in the system.")
        self.student_id = student_id