"""Environmental storage condition model."""

from constants import (
    DEFAULT_HUMIDITY_PERCENT,
    DEFAULT_TARGET_TEMP_C,
    DEFAULT_TEMP_TOLERANCE_C,
    MAX_TEMPERATURE_C,
    MIN_TEMPERATURE_C,
)
from exceptions import InvalidDataError


class StorageCondition:
    """Defines required temperature and humidity parameters for storage."""

    def __init__(
        self,
        min_temp_c: float = DEFAULT_TARGET_TEMP_C - DEFAULT_TEMP_TOLERANCE_C,
        max_temp_c: float = DEFAULT_TARGET_TEMP_C + DEFAULT_TEMP_TOLERANCE_C,
        max_humidity_percent: float = DEFAULT_HUMIDITY_PERCENT,
        requires_ventilation: bool = False,
    ) -> None:
        if min_temp_c > max_temp_c:
            raise InvalidDataError("Minimum temperature cannot exceed maximum.")
        if min_temp_c < MIN_TEMPERATURE_C or max_temp_c > MAX_TEMPERATURE_C:
            raise InvalidDataError("Temperature limits are out of physical bounds.")
        self.min_temp_c = min_temp_c
        self.max_temp_c = max_temp_c
        self.max_humidity_percent = max_humidity_percent
        self.requires_ventilation = requires_ventilation

    def is_temperature_acceptable(self, current_temp_c: float) -> bool:
        """Check if a measured temperature falls within allowed bounds."""
        return self.min_temp_c <= current_temp_c <= self.max_temp_c

    def is_compatible_with(self, other: "StorageCondition") -> bool:
        """Check whether two storage conditions have an overlapping temperature range."""
        overlap_min = max(self.min_temp_c, other.min_temp_c)
        overlap_max = min(self.max_temp_c, other.max_temp_c)
        return overlap_min <= overlap_max