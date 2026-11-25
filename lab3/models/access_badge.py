"""Security access badge model for warehouse personnel."""

from exceptions import InvalidDataError


class AccessBadge:
    """Represents an electronic pass granting access to warehouse zones."""

    def __init__(self, badge_id: str, clearance_level: int) -> None:
        if not badge_id or not 1 <= clearance_level <= 5:
            raise InvalidDataError("Badge ID is required and clearance must be 1-5.")
        self.badge_id = badge_id
        self.clearance_level = clearance_level
        self.is_active = True

    def deactivate(self) -> None:
        """Disable the badge so it can no longer be used for entry."""
        self.is_active = False

    def upgrade_clearance(self, new_level: int) -> None:
        """Increase the clearance level of an active badge."""
        if not self.is_active or not self.clearance_level < new_level <= 5:
            raise InvalidDataError("Cannot upgrade inactive badge or invalid level.")
        self.clearance_level = new_level