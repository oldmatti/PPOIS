"""Product category model with default storage requirements."""

from exceptions import InvalidDataError
from .storage_condition import StorageCondition


class ProductCategory:
    """Groups products sharing common storage and handling rules."""

    def __init__(
        self,
        category_id: str,
        name: str,
        default_condition: StorageCondition,
        requires_certification: bool = False,
    ) -> None:
        if not category_id or not name:
            raise InvalidDataError("Category ID and name are required.")
        self.category_id = category_id
        self.name = name
        self.default_condition = default_condition
        self.requires_certification = requires_certification

    def is_compatible_with_condition(self, condition: StorageCondition) -> bool:
        """Check whether a zone storage condition suits this category."""
        return self.default_condition.is_compatible_with(condition)

    def update_storage_condition(self, new_condition: StorageCondition) -> None:
        """Replace the default storage condition for the category."""
        self.default_condition = new_condition