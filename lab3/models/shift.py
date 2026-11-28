"""Work shift model for warehouse staff scheduling."""

from constants import DEFAULT_SHIFT_HOURS, MAX_SHIFT_HOURS
from exceptions import InvalidDataError


class Shift:
    """Represents a scheduled work shift with duration limits."""

    def __init__(
        self,
        shift_id: str,
        shift_type: str,
        duration_hours: int = DEFAULT_SHIFT_HOURS,
    ) -> None:
        if not shift_id or shift_type not in ("day", "night", "swing"):
            raise InvalidDataError("Invalid shift ID or shift type.")
        if not 1 <= duration_hours <= MAX_SHIFT_HOURS:
            raise InvalidDataError(f"Shift duration must be 1-{MAX_SHIFT_HOURS} hours.")
        self.shift_id = shift_id
        self.shift_type = shift_type
        self.duration_hours = duration_hours
        self.is_closed = False

    def extend_shift(self, extra_hours: int) -> None:
        """Extend the shift duration without exceeding the legal maximum."""
        if self.is_closed or extra_hours <= 0:
            raise InvalidDataError("Cannot extend a closed shift or by non-positive hours.")
        if self.duration_hours + extra_hours > MAX_SHIFT_HOURS:
            raise InvalidDataError("Shift extension exceeds maximum allowed hours.")
        self.duration_hours += extra_hours

    def close_shift(self) -> None:
        """Mark the shift as completed."""
        self.is_closed = True