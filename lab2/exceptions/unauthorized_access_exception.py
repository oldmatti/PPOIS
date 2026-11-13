from .deanery_exception import DeaneryException

class UnauthorizedAccessException(DeaneryException):
    def __init__(self, role: str, action: str):
        super().__init__(f"Access denied: role '{role}' does not have permission to perform '{action}'.")