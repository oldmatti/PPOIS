"""Unit tests for Selection Sort, Bucket Sort, and the Product model."""

from array import array
import unittest

from lab4.sorting import Product, bucket_sort, selection_sort


class TestProduct(unittest.TestCase):
    """Tests for the custom Product class."""

    def test_valid_product_and_comparisons(self) -> None:
        """Verify product creation, equality, ordering, and string formatting."""
        cheap = Product("Mouse", 20.0, 4.5)
        same_cheap = Product("Mouse", 20.0, 4.5)
        expensive = Product("Monitor", 200.0, 4.8)

        self.assertEqual(cheap, same_cheap)
        self.assertNotEqual(cheap, expensive)
        self.assertLess(cheap, expensive)
        self.assertNotEqual(cheap, "not a product")
        self.assertIn("Mouse", repr(cheap))

    def test_invalid_product_raises_value_error(self) -> None:
        """Verify validation rejects empty name, negative price, and bad rating."""
        with self.assertRaises(ValueError):
            Product("   ", 10.0, 4.0)
        with self.assertRaises(ValueError):
            Product("Cable", -5.0, 4.0)
        with self.assertRaises(ValueError):
            Product("Cable", 10.0, 6.0)


class TestSelectionSort(unittest.TestCase):
    """Tests for the generic selection_sort function."""

    def test_sort_integers_and_reverse(self) -> None:
        """Verify ascending and descending sorting of integer lists."""
        data = [64, 25, 12, 22, 11]
        self.assertEqual(selection_sort(data), [11, 12, 22, 25, 64])
        self.assertEqual(selection_sort(data, reverse=True), [64, 25, 22, 12, 11])
        # Исходный список не должен изменяться
        self.assertEqual(data, [64, 25, 12, 22, 11])

    def test_sort_array_and_tuple_preserve_type(self) -> None:
        """Verify sorting preserves array.array and tuple collection types."""
        arr = array("i", [5, 1, 4, 2, 3])
        sorted_arr = selection_sort(arr)
        self.assertIsInstance(sorted_arr, array)
        self.assertEqual(list(sorted_arr), [1, 2, 3, 4, 5])

        tup = (3, 1, 2)
        sorted_tup = selection_sort(tup)
        self.assertIsInstance(sorted_tup, tuple)
        self.assertEqual(sorted_tup, (1, 2, 3))

    def test_sort_empty_and_single_element(self) -> None:
        """Verify edge cases with empty and single-element collections."""
        self.assertEqual(selection_sort([]), [])
        self.assertEqual(selection_sort([42]), [42])

    def test_sort_custom_objects_with_and_without_key(self) -> None:
        """Verify sorting of Product objects by default order and by key."""
        products = [
            Product("Keyboard", 75.0, 4.6),
            Product("Mouse", 25.0, 4.9),
            Product("Monitor", 300.0, 4.2),
        ]
        by_price = selection_sort(products)
        self.assertEqual([item.name for item in by_price], ["Mouse", "Keyboard", "Monitor"])

        by_rating = selection_sort(products, key=lambda item: item.rating, reverse=True)
        self.assertEqual([item.name for item in by_rating], ["Mouse", "Keyboard", "Monitor"])


class TestBucketSort(unittest.TestCase):
    """Tests for the generic bucket_sort function."""

    def test_sort_numbers_and_reverse(self) -> None:
        """Verify ascending and descending bucket sort on numeric lists."""
        data = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]
        self.assertEqual(bucket_sort(data), sorted(data))
        self.assertEqual(bucket_sort(data, reverse=True), sorted(data, reverse=True))

    def test_sort_array_tuple_and_duplicates(self) -> None:
        """Verify bucket sort preserves types and handles identical values."""
        arr = array("d", [3.5, 1.2, 4.8, 0.9])
        sorted_arr = bucket_sort(arr)
        self.assertIsInstance(sorted_arr, array)
        self.assertEqual(list(sorted_arr), [0.9, 1.2, 3.5, 4.8])

        self.assertEqual(bucket_sort((5, 5, 5)), (5, 5, 5))
        self.assertEqual(bucket_sort([]), [])
        self.assertEqual(bucket_sort([7]), [7])

    def test_sort_custom_objects_by_numeric_key(self) -> None:
        """Verify bucket sort on Product objects using a numeric key."""
        products = [
            Product("Keyboard", 75.0, 4.6),
            Product("Mouse", 25.0, 4.9),
            Product("Monitor", 300.0, 4.2),
        ]
        sorted_products = bucket_sort(products, key=lambda item: item.price)
        self.assertEqual([item.name for item in sorted_products], ["Mouse", "Keyboard", "Monitor"])

    def test_invalid_arguments_raise_errors(self) -> None:
        """Verify invalid bucket count and non-numeric items raise errors."""
        with self.assertRaises(ValueError):
            bucket_sort([1, 2, 3], bucket_count=0)
        with self.assertRaises(TypeError):
            bucket_sort(["apple", "banana"])


if __name__ == "__main__":
    unittest.main()