"""Generic Bucket Sort implementation supporting lists and arrays."""

from __future__ import annotations

from array import array
from typing import Callable, List, Optional, Sequence, TypeVar

from lab4.constants import (
    DEFAULT_BUCKET_COUNT,
    MIN_COLLECTION_LENGTH_TO_SORT,
    ZERO_RANGE_THRESHOLD,
)
from lab4.sorting.selection_sort import selection_sort

ElementType = TypeVar("ElementType")
NumericKeyFunction = Callable[[ElementType], float]


def _get_numeric_value(
    item: ElementType,
    key: Optional[NumericKeyFunction[ElementType]],
) -> float:
    """Extract a numeric value from an item for bucket distribution."""
    raw_value = key(item) if key is not None else item
    if not isinstance(raw_value, (int, float)):
        raise TypeError(
            "Bucket sort requires numeric values or a key function returning int/float."
        )
    return float(raw_value)


def _compute_bucket_index(
    numeric_value: float,
    min_value: float,
    value_range: float,
    bucket_count: int,
) -> int:
    """Calculate the destination bucket index for a given numeric value."""
    normalized = (numeric_value - min_value) / value_range
    bucket_index = int(normalized * bucket_count)
    # Граничный максимум отправляем в последнюю корзину
    return min(bucket_index, bucket_count - 1)


def _distribute_into_buckets(
    items: List[ElementType],
    key: Optional[NumericKeyFunction[ElementType]],
    bucket_count: int,
) -> List[List[ElementType]]:
    """Distribute elements across buckets based on their numeric keys."""
    numeric_values = [_get_numeric_value(item, key) for item in items]
    min_value = min(numeric_values)
    max_value = max(numeric_values)
    value_range = max_value - min_value

    # Если все ключи одинаковы, распределение не требуется
    if value_range == ZERO_RANGE_THRESHOLD:
        return [items]

    buckets: List[List[ElementType]] = [[] for _ in range(bucket_count)]
    for item, numeric_value in zip(items, numeric_values):
        index = _compute_bucket_index(numeric_value, min_value, value_range, bucket_count)
        buckets[index].append(item)
    return buckets


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


def bucket_sort(
    collection: Sequence[ElementType],
    *,
    key: Optional[NumericKeyFunction[ElementType]] = None,
    reverse: bool = False,
    bucket_count: int = DEFAULT_BUCKET_COUNT,
) -> Sequence[ElementType]:
    """Sort a list, array, or sequence using the Bucket Sort algorithm."""
    if bucket_count < 1:
        raise ValueError("Bucket count must be a positive integer.")

    working_items = list(collection)
    if len(working_items) < MIN_COLLECTION_LENGTH_TO_SORT:
        return _wrap_result(collection, working_items)

    buckets = _distribute_into_buckets(working_items, key, bucket_count)
    ordered_buckets = reversed(buckets) if reverse else buckets

    # Сортируем каждую непустую корзину и объединяем результат
    sorted_items: List[ElementType] = []
    for bucket in ordered_buckets:
        if bucket:
            sorted_bucket = selection_sort(bucket, key=key, reverse=reverse)
            sorted_items.extend(sorted_bucket)

    return _wrap_result(collection, sorted_items)