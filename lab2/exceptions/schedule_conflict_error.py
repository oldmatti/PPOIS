from .deanery_exception import DeaneryException

class ScheduleConflictError(DeaneryException):
    """Raised when there is a room or time conflict in the schedule."""
    pass