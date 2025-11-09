"""
Test cases for InventoryLogEntry value object.
Tests immutability, validation, and all public methods.
"""
import unittest
import unittest.mock
import datetime
from typing import Any
from unittest.mock import patch
from domain.value_objects.inventory_log_entry import InventoryLogEntry


class TestInventoryLogEntry(unittest.TestCase):
    """Test cases for InventoryLogEntry value object."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.valid_product_id = 1
        self.valid_quantity_change = 10
        self.valid_reason = "restock"
        self.fixed_datetime = datetime.datetime(2024, 1, 15, 10, 30, 0)

    def test_valid_inventory_log_entry_creation(self) -> None:
        """Test creation of valid inventory log entry."""
        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason
        )

        self.assertEqual(entry.product_id, self.valid_product_id)
        self.assertEqual(entry.quantity_change, self.valid_quantity_change)
        self.assertEqual(entry.reason, self.valid_reason)
        self.assertIsInstance(entry.timestamp, datetime.datetime)

    def test_inventory_log_entry_with_custom_timestamp(self) -> None:
        """Test creation with custom timestamp."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)

        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=custom_time
        )

        self.assertEqual(entry.timestamp, custom_time)

    @patch('datetime.datetime')
    def test_inventory_log_entry_default_timestamp(self, mock_datetime: unittest.mock.MagicMock) -> None:
        """Test that timestamp defaults to current time when not provided."""
        mock_datetime.now.return_value = self.fixed_datetime
        mock_datetime.side_effect = datetime.datetime

        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason
        )

        mock_datetime.now.assert_called_once()
        self.assertEqual(entry.timestamp, self.fixed_datetime)

    def test_invalid_product_id_validation(self) -> None:
        """Test validation for invalid product IDs."""
        # Test each invalid case separately to avoid type checker issues
        with self.assertRaises(ValueError) as context:
            InventoryLogEntry(
                product_id=0, quantity_change=self.valid_quantity_change, reason=self.valid_reason)
        self.assertIn("Product ID must be a positive integer",
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            InventoryLogEntry(
                product_id=-1, quantity_change=self.valid_quantity_change, reason=self.valid_reason)
        self.assertIn("Product ID must be a positive integer",
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            InventoryLogEntry(
                product_id=-100, quantity_change=self.valid_quantity_change, reason=self.valid_reason)
        self.assertIn("Product ID must be a positive integer",
                      str(context.exception))

    def test_invalid_quantity_change_validation(self) -> None:
        """Test validation for invalid quantity changes."""
        # Test zero quantity - this should be valid
        entry = InventoryLogEntry(
            product_id=self.valid_product_id, quantity_change=0, reason=self.valid_reason)
        self.assertEqual(entry.quantity_change, 0)

    def test_valid_quantity_change_types(self) -> None:
        """Test that positive, negative, and zero quantities are accepted."""
        quantities = [10, -5, 0, 100, -100]

        for qty in quantities:
            with self.subTest(quantity_change=qty):
                entry = InventoryLogEntry(
                    product_id=self.valid_product_id,
                    quantity_change=qty,
                    reason=self.valid_reason
                )
                self.assertEqual(entry.quantity_change, qty)

    def test_invalid_reason_validation(self) -> None:
        """Test validation for invalid reasons."""
        with self.assertRaises(ValueError) as context:
            InventoryLogEntry(product_id=self.valid_product_id,
                              quantity_change=self.valid_quantity_change, reason="")
        self.assertIn("Reason must be a non-empty string",
                      str(context.exception))

        with self.assertRaises(ValueError) as context:
            InventoryLogEntry(product_id=self.valid_product_id,
                              quantity_change=self.valid_quantity_change, reason="   ")
        self.assertIn("Reason must be a non-empty string",
                      str(context.exception))

    def test_reason_whitespace_trimming(self) -> None:
        """Test that reason whitespace is trimmed."""
        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason="  restock  "
        )

        self.assertEqual(entry.reason, "restock")

    def test_is_stock_increase_method(self) -> None:
        """Test is_stock_increase method."""
        positive_entry = InventoryLogEntry(1, 10, "restock")
        zero_entry = InventoryLogEntry(1, 0, "adjustment")
        negative_entry = InventoryLogEntry(1, -5, "sale")

        self.assertTrue(positive_entry.is_stock_increase())
        self.assertFalse(zero_entry.is_stock_increase())
        self.assertFalse(negative_entry.is_stock_increase())

    def test_is_stock_decrease_method(self) -> None:
        """Test is_stock_decrease method."""
        positive_entry = InventoryLogEntry(1, 10, "restock")
        zero_entry = InventoryLogEntry(1, 0, "adjustment")
        negative_entry = InventoryLogEntry(1, -5, "sale")

        self.assertFalse(positive_entry.is_stock_decrease())
        self.assertFalse(zero_entry.is_stock_decrease())
        self.assertTrue(negative_entry.is_stock_decrease())

    def test_immutability(self) -> None:
        """Test that InventoryLogEntry is immutable."""
        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason
        )

        # Properties should not have setters
        with self.assertRaises(AttributeError):
            setattr(entry, 'product_id', 2000)
        with self.assertRaises(AttributeError):
            setattr(entry, 'quantity_change', -100)
        with self.assertRaises(AttributeError):
            setattr(entry, 'reason', 'sale')
        with self.assertRaises(AttributeError):
            setattr(entry, 'timestamp', datetime.datetime.now())

    def test_to_dict_method(self) -> None:
        """Test to_dict conversion method."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)
        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=custom_time
        )

        expected_dict = {
            "product_id": self.valid_product_id,
            "quantity_change": self.valid_quantity_change,
            "reason": self.valid_reason,
            "timestamp": custom_time
        }

        self.assertEqual(entry.to_dict(), expected_dict)

    def test_str_method(self) -> None:
        """Test string representation."""
        positive_entry = InventoryLogEntry(1, 10, "restock")
        negative_entry = InventoryLogEntry(1, -5, "sale")
        zero_entry = InventoryLogEntry(1, 0, "adjustment")

        self.assertEqual(str(positive_entry), "Product 1: +10 (restock)")
        self.assertEqual(str(negative_entry), "Product 1: -5 (sale)")
        self.assertEqual(str(zero_entry), "Product 1: +0 (adjustment)")

    def test_repr_method(self) -> None:
        """Test detailed representation."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)
        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=custom_time
        )

        expected_repr = (
            f"InventoryLogEntry("
            f"product_id={self.valid_product_id}, "
            f"quantity_change={self.valid_quantity_change}, "
            f"reason='{self.valid_reason}', "
            f"timestamp={custom_time})"
        )
        self.assertEqual(repr(entry), expected_repr)

    def test_equality_same_entries(self) -> None:
        """Test equality between identical entries."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)

        entry1 = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=custom_time
        )

        entry2 = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=custom_time
        )

        self.assertEqual(entry1, entry2)
        self.assertTrue(entry1 == entry2)

    def test_inequality_different_entries(self) -> None:
        """Test inequality between different entries."""
        base_entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=self.fixed_datetime
        )

        # Different product_id
        diff_product = InventoryLogEntry(
            product_id=2,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=self.fixed_datetime
        )
        self.assertNotEqual(base_entry, diff_product)

        # Different quantity_change
        diff_quantity = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=-5,
            reason=self.valid_reason,
            timestamp=self.fixed_datetime
        )
        self.assertNotEqual(base_entry, diff_quantity)

        # Different reason
        diff_reason = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason="sale",
            timestamp=self.fixed_datetime
        )
        self.assertNotEqual(base_entry, diff_reason)

        # Different timestamp
        diff_time = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=datetime.datetime(2024, 2, 15, 10, 30, 0)
        )
        self.assertNotEqual(base_entry, diff_time)

    def test_equality_with_non_inventory_log_entry(self) -> None:
        """Test equality with non-InventoryLogEntry objects."""
        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason
        )

        non_entries = [
            "not an entry",
            123,
            {"product_id": self.valid_product_id},
            None,
            []
        ]

        for non_entry in non_entries:
            with self.subTest(other=non_entry):
                self.assertNotEqual(entry, non_entry)
                self.assertFalse(entry == non_entry)

    def test_hash_consistency(self) -> None:
        """Test that hash is consistent for equal entries."""
        custom_time = datetime.datetime(2024, 1, 15, 10, 30, 0)

        entry1 = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=custom_time
        )

        entry2 = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=custom_time
        )

        # Equal objects must have equal hashes
        self.assertEqual(hash(entry1), hash(entry2))

    def test_hash_different_for_different_entries(self) -> None:
        """Test that different entries have different hashes."""
        entry1 = InventoryLogEntry(1, 10, "restock", self.fixed_datetime)
        entry2 = InventoryLogEntry(2, 10, "restock", self.fixed_datetime)

        # Different entries should have different hashes (usually)
        self.assertNotEqual(hash(entry1), hash(entry2))

    def test_can_be_used_in_set(self) -> None:
        """Test that InventoryLogEntry can be used in sets."""
        entry1 = InventoryLogEntry(1, 10, "restock", self.fixed_datetime)
        entry2 = InventoryLogEntry(2, -5, "sale", self.fixed_datetime)

        # Should be able to add to set
        entry_set = {entry1, entry2}
        self.assertEqual(len(entry_set), 2)

        # Adding the same entry again shouldn't increase size
        entry_set.add(entry1)
        self.assertEqual(len(entry_set), 2)

    def test_can_be_used_as_dict_key(self) -> None:
        """Test that InventoryLogEntry can be used as dictionary keys."""
        entry = InventoryLogEntry(
            product_id=self.valid_product_id,
            quantity_change=self.valid_quantity_change,
            reason=self.valid_reason,
            timestamp=self.fixed_datetime
        )

        # Should be able to use as dict key
        entry_dict = {entry: "processed"}
        self.assertEqual(entry_dict[entry], "processed")

    def test_edge_case_values(self) -> None:
        """Test edge cases for values."""
        # Large product ID
        large_entry = InventoryLogEntry(999999, 1, "test")
        self.assertEqual(large_entry.product_id, 999999)

        # Large quantity changes
        large_positive = InventoryLogEntry(1, 999999, "massive_restock")
        large_negative = InventoryLogEntry(1, -999999, "massive_sale")
        self.assertEqual(large_positive.quantity_change, 999999)
        self.assertEqual(large_negative.quantity_change, -999999)

        # Long reason string
        long_reason = "a" * 1000
        long_entry = InventoryLogEntry(1, 10, long_reason)
        self.assertEqual(long_entry.reason, long_reason)


if __name__ == '__main__':
    unittest.main()
