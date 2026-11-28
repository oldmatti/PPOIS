"""Warehouse security checkpoint model."""

from typing import List

from exceptions import InvalidDataError, UnauthorizedAccessError


class SecurityCheckpoint:
    """Controls vehicle and personnel entry at the warehouse perimeter."""

    def __init__(self, checkpoint_id: str, required_clearance: int) -> None:
        if not checkpoint_id or required_clearance < 1:
            raise InvalidDataError("Checkpoint ID and positive clearance are required.")
        self.checkpoint_id = checkpoint_id
        self.required_clearance = required_clearance
        self.access_log: List[str] = []
        self.is_active = True

    def verify_entry(self, badge_id: str, clearance_level: int) -> bool:
        """Validate clearance level and log entry or raise an error."""
        if not self.is_active:
            raise UnauthorizedAccessError(f"Checkpoint {self.checkpoint_id} is closed.")
        if clearance_level < self.required_clearance:
            raise UnauthorizedAccessError(f"Badge {badge_id} has insufficient clearance.")
        self.access_log.append(f"GRANTED:{badge_id}")
        return True

    def log_vehicle_passage(self, vehicle_plate: str, direction: str) -> None:
        """Record an inbound or outbound vehicle passage."""
        if direction not in ("in", "out"):
            raise InvalidDataError("Direction must be 'in' or 'out'.")
        self.access_log.append(f"VEHICLE:{direction.upper()}:{vehicle_plate}")