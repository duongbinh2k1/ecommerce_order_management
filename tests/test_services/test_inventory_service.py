"""
Test InventoryService - inventory management and stock operations
Tests inventory logging, restocking, and stock availability checks
"""
import unittest
from unittest.mock import Mock
from services.inventory_service import InventoryService
from domain.value_objects.inventory_log_entry import InventoryLogEntry


class TestInventoryService(unittest.TestCase):
    """Test InventoryService inventory management functionality."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.product_service = Mock()
        self.inventory_service = InventoryService(self.product_service)

        # Create mock product
        self.product = Mock()
        self.product.product_id = 1
        self.product.name = "Test Product"
        self.product.quantity_available = 50
        self.product.supplier_id = 1

    def test_log_inventory_change(self) -> None:
        """Test logging inventory changes."""
        self.inventory_service.log_inventory_change(
            1, 10, "restock"
        )

        logs = self.inventory_service.get_inventory_logs()
        self.assertEqual(len(logs), 1)

        log_entry = logs[0]
        self.assertIsInstance(log_entry, InventoryLogEntry)
        self.assertEqual(log_entry.product_id, 1)
        self.assertEqual(log_entry.quantity_change, 10)
        self.assertEqual(log_entry.reason, "restock")
        self.assertIsNotNone(log_entry.timestamp)

    def test_restock_product_success(self) -> None:
        """Test successful product restocking."""
        self.product_service.get_product.return_value = self.product

        result = self.inventory_service.restock_product(1, 20)

        self.assertTrue(result)
        self.product_service.get_product.assert_called_once_with(1)
        self.product_service.update_product_quantity.assert_called_once_with(
            1, 70  # 50 + 20
        )

        # Check log was created
        logs = self.inventory_service.get_inventory_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0].reason, "restock")

    def test_restock_product_not_found(self) -> None:
        """Test restocking non-existent product."""
        self.product_service.get_product.return_value = None

        result = self.inventory_service.restock_product(999, 20)

        self.assertFalse(result)
        self.product_service.get_product.assert_called_once_with(999)
        self.product_service.update_product_quantity.assert_not_called()

    def test_restock_product_supplier_mismatch(self) -> None:
        """Test restocking with wrong supplier."""
        self.product_service.get_product.return_value = self.product

        result = self.inventory_service.restock_product(
            1, 20, 999
        )

        self.assertFalse(result)
        self.product_service.update_product_quantity.assert_not_called()

    def test_restock_product_with_correct_supplier(self) -> None:
        """Test restocking with correct supplier."""
        self.product_service.get_product.return_value = self.product

        result = self.inventory_service.restock_product(
            1, 15, 1
        )

        self.assertTrue(result)
        self.product_service.update_product_quantity.assert_called_once_with(
            1, 65  # 50 + 15
        )

    def test_get_low_stock_products_default_threshold(self) -> None:
        """Test getting low stock products with default threshold."""
        low_stock_product = Mock()
        low_stock_product.quantity_available = 5

        normal_stock_product = Mock()
        normal_stock_product.quantity_available = 15

        self.product_service.get_all_products.return_value = {
            1: low_stock_product,
            2: normal_stock_product
        }

        low_stock = self.inventory_service.get_low_stock_products()

        self.assertEqual(len(low_stock), 1)
        self.assertEqual(low_stock[0], low_stock_product)

    def test_get_low_stock_products_custom_threshold(self) -> None:
        """Test getting low stock products with custom threshold."""
        product1 = Mock()
        product1.quantity_available = 5

        product2 = Mock()
        product2.quantity_available = 15

        product3 = Mock()
        product3.quantity_available = 25

        self.product_service.get_all_products.return_value = {
            1: product1,
            2: product2,
            3: product3
        }

        # Test with threshold of 20
        low_stock = self.inventory_service.get_low_stock_products(20)

        self.assertEqual(len(low_stock), 2)  # Products with 5 and 15 quantity

    def test_get_low_stock_products_no_low_stock(self) -> None:
        """Test getting low stock products when none are low."""
        product1 = Mock()
        product1.quantity_available = 50

        product2 = Mock()
        product2.quantity_available = 100

        self.product_service.get_all_products.return_value = {
            1: product1,
            2: product2
        }

        low_stock = self.inventory_service.get_low_stock_products()

        self.assertEqual(len(low_stock), 0)

    def test_check_product_availability_sufficient_stock(self) -> None:
        """Test checking product availability with sufficient stock."""
        self.product_service.get_product.return_value = self.product

        available = self.inventory_service.check_product_availability(
            1, 30
        )

        self.assertTrue(available)
        self.product_service.get_product.assert_called_once_with(1)

    def test_check_product_availability_insufficient_stock(self) -> None:
        """Test checking product availability with insufficient stock."""
        self.product_service.get_product.return_value = self.product

        available = self.inventory_service.check_product_availability(
            1, 100  # More than the 50 available
        )

        self.assertFalse(available)

    def test_check_product_availability_exact_stock(self) -> None:
        """Test checking product availability with exact stock."""
        self.product_service.get_product.return_value = self.product

        available = self.inventory_service.check_product_availability(
            1, 50  # Exactly the amount available
        )

        self.assertTrue(available)

    def test_check_product_availability_product_not_found(self) -> None:
        """Test checking availability for non-existent product."""
        self.product_service.get_product.return_value = None

        available = self.inventory_service.check_product_availability(
            999, 10
        )

        self.assertFalse(available)

    def test_get_inventory_logs_returns_copy(self) -> None:
        """Test that get_inventory_logs returns a copy."""
        self.inventory_service.log_inventory_change(1, 10, "test")

        logs1 = self.inventory_service.get_inventory_logs()
        logs2 = self.inventory_service.get_inventory_logs()

        # Should be equal but not the same object
        self.assertEqual(logs1, logs2)
        self.assertIsNot(logs1, logs2)

        # Modifying returned logs shouldn't affect internal state
        logs1.append(Mock())  # Can't append dict to list of InventoryLogEntry
        logs3 = self.inventory_service.get_inventory_logs()
        self.assertNotEqual(len(logs1), len(logs3))

    def test_multiple_inventory_changes(self) -> None:
        """Test logging multiple inventory changes."""
        self.inventory_service.log_inventory_change(1, 10, "restock")
        self.inventory_service.log_inventory_change(2, -5, "sale")
        self.inventory_service.log_inventory_change(1, 20, "initial_stock")

        logs = self.inventory_service.get_inventory_logs()
        self.assertEqual(len(logs), 3)

        # Check all entries are different
        reasons = [log.reason for log in logs]
        self.assertIn("restock", reasons)
        self.assertIn("sale", reasons)
        self.assertIn("initial_stock", reasons)

    def test_get_inventory_logs_as_dicts_backward_compatibility(self) -> None:
        """Test backward compatibility method returns dictionaries."""
        self.inventory_service.log_inventory_change(1, 10, "restock")
        self.inventory_service.log_inventory_change(2, -5, "sale")

        # Test value object method
        logs = self.inventory_service.get_inventory_logs()
        self.assertEqual(len(logs), 2)
        self.assertIsInstance(logs[0], InventoryLogEntry)

        # Test backward compatibility method
        dict_logs = self.inventory_service.get_inventory_logs_as_dicts()
        self.assertEqual(len(dict_logs), 2)
        self.assertIsInstance(dict_logs[0], dict)
        
        # Check dictionary structure
        first_log = dict_logs[0]
        self.assertEqual(first_log['product_id'], 1)
        self.assertEqual(first_log['quantity_change'], 10)
        self.assertEqual(first_log['reason'], "restock")
        self.assertIn('timestamp', first_log)


if __name__ == '__main__':
    unittest.main()