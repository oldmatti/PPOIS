from .deanery_exception import DeaneryException

class InvalidGroupTransferException(DeaneryException):
    def __init__(self, student_name: str, target_group: str):
        super().__init__(f"Cannot transfer student {student_name} to group {target_group}. Group is full or major mismatch.")