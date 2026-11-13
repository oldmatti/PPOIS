from .deanery_exception import DeaneryException

class InvalidGradeError(DeaneryException):
    """Raised when a grade value is outside the allowed range."""
    pass