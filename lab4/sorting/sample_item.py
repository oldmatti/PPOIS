"""Custom domain class for demonstrating generic sorting algorithms."""

from __future__ import annotations

from functools import total_ordering

from lab4.constants import (
    MAX_PRODUCT_RATING,
    MIN_PRODUCT_PRICE,
    MIN_PRODUCT_RATING,
)


@total_ordering
class Product:
    """Represent a store product that can be compared and sorted."""

    def __init__(self, name: str, price: float, rating: float) -> None:
        """Initialize a product with validated name, price, and rating."""
        if not name.strip():
            raise ValueError("Product name must not be empty.")
        if price < MIN_PRODUCT_PRICE:
            raise ValueError("Product price cannot be negative.")
        if not (MIN_PRODUCT_RATING <= rating <= MAX_PRODUCT_RATING):
            raise ValueError("Product rating must be between 0.0 and 5.0.")

        # сохранение очищенного названия и числовых характеристик товара
        self.name = name.strip()
        self.price = float(price)
        self.rating = float(rating)

    def __eq__(self, other: object) -> bool:
        """Check equality based on price, rating, and name."""
        if not isinstance(other, Product):
            return NotImplemented
        return (
            self.price == other.price
            and self.rating == other.rating
            and self.name == other.name
        )

    def __lt__(self, other: object) -> bool:
        """Compare products primarily by price, then by name."""
        if not isinstance(other, Product):
            return NotImplemented
        return (self.price, self.name) < (other.price, other.name)

    def __repr__(self) -> str:
        """Return a readable string representation of the product."""
        return (
            f"Product(name='{self.name}', "
            f"price={self.price:.2f}, rating={self.rating:.1f})"
        )