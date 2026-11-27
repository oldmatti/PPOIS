"""Bidirectional, reverse, and read-only iterators for the graph container."""

from __future__ import annotations

from typing import Generic, List, Sequence, TypeVar

from lab4.constants import INVALID_ITERATOR_INDEX
from lab4.exceptions import InvalidIteratorError

ItemType = TypeVar("ItemType")


class BidirectionalIterator(Generic[ItemType]):
    """Generic bidirectional iterator supporting reverse and const modes."""

    def __init__(
        self,
        items: Sequence[ItemType],
        *,
        is_reverse: bool = False,
        is_const: bool = False,
        owner_id: int = 0,
    ) -> None:
        """Initialize iterator over a snapshot of graph items."""
        # Сохраняем снимок элементов в прямом или обратном порядке
        self._items: List[ItemType] = list(reversed(items)) if is_reverse else list(items)
        self._index: int = INVALID_ITERATOR_INDEX
        self._is_reverse = is_reverse
        self._is_const = is_const
        self._owner_id = owner_id

    @property
    def is_const(self) -> bool:
        """Return True if the iterator is read-only."""
        return self._is_const

    @property
    def is_reverse(self) -> bool:
        """Return True if the iterator traverses items in reverse order."""
        return self._is_reverse

    @property
    def owner_id(self) -> int:
        """Return the identifier of the graph that created this iterator."""
        return self._owner_id

    def has_next(self) -> bool:
        """Return True if moving forward yields a valid item."""
        return self._index + 1 < len(self._items)

    def has_prev(self) -> bool:
        """Return True if moving backward yields a valid item."""
        return self._index > 0

    def current(self) -> ItemType:
        """Return the element at the current iterator position."""
        if not (0 <= self._index < len(self._items)):
            raise InvalidIteratorError("Iterator does not point to a valid element.")
        return self._items[self._index]

    def next_item(self) -> ItemType:
        """Advance the iterator one step forward and return the element."""
        if not self.has_next():
            raise StopIteration("Iterator reached the end of the sequence.")
        self._index += 1
        return self._items[self._index]

    def prev_item(self) -> ItemType:
        """Move the iterator one step backward and return the element."""
        if not self.has_prev():
            raise StopIteration("Iterator reached the beginning of the sequence.")
        self._index -= 1
        return self._items[self._index]

    def __iter__(self) -> BidirectionalIterator[ItemType]:
        """Return the iterator object itself for Python's iteration protocol."""
        return self

    def __next__(self) -> ItemType:
        """Advance forward as required by Python's iterator protocol."""
        return self.next_item()