"""Generic Selection Sort implementation supporting lists and arrays."""

from __future__ import annotations

from array import array
from typing import Any, Callable, List, Optional, Sequence, TypeVar

from lab4.constants import MIN_COLLECTION_LENGTH_TO_SORT

ElementType = TypeVar("ElementType")
KeyFunction = Callable[[ElementType], Any]


def _extract_key(item: ElementType, key: Optional[KeyFunction[ElementType]]) -> Any:
    """Return comparison key for an item using the optional key function."""
    return key(item) if key is not None else item


def _find_extreme_index(
    items: List[ElementType],
    start_index: int,
    key: Optional[KeyFunction[ElementType]],
    reverse: bool,
) -> int:
    """Find the index of the minimum (or maximum if reversed) element."""
    extreme_index = start_index
    extreme_key = _extract_key(items[extreme_index], key)

    # ишем индекс минимального или максимального элемента в неотсортированной части
    for current_index in range(start_index + 1, len(items)):
        current_key = _extract_key(items[current_index], key)
        is_better = current_key > extreme_key if reverse else current_key < extreme_key
        if is_better:
            extreme_index = current_index
            extreme_key = current_key

    return extreme_index


def _wrap_result(
    original: Sequence[ElementType],
    sorted_items: List[ElementType],
) -> Sequence[ElementType]:
    """Return sorted items in the same collection type as the input."""
    if isinstance(original, array):
        return array(original.typecode, sorted_items)
    if isinstance(original, tuple):
        return tuple(sorted_items)
    return sorted_items


def selection_sort(
    collection: Sequence[ElementType],
    *,
    key: Optional[KeyFunction[ElementType]] = None,
    reverse: bool = False,
) -> Sequence[ElementType]:
    """Sort a list, array, or sequence using the Selection Sort algorithm."""
    working_items = list(collection)
    if len(working_items) < MIN_COLLECTION_LENGTH_TO_SORT:
        return _wrap_result(collection, working_items)

    # Пошагово ставим найденный экстремум на текущую позицию
    for current_position in range(len(working_items) - 1):
        target_index = _find_extreme_index(working_items, current_position, key, reverse)
        if target_index != current_position:
            working_items[current_position], working_items[target_index] = (
                working_items[target_index],
                working_items[current_position],
            )

    return _wrap_result(collection, working_items)
