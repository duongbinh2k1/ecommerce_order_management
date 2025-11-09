"""
Tests for Data Loader Service
"""
import unittest
import tempfile
import os
import datetime
from application.order_processor import OrderProcessor
from data_loader import DataLoaderService


class TestDataLoaderService(unittest.TestCase):
    """Test cases for DataLoaderService."""

    def setUp(self) -> None:
        """Set up test environment."""
        self.order_processor = OrderProcessor()
        self.data_loader = DataLoaderService(self.order_processor)
        
        # Setup test data
        self._setup_test_data()

    def _setup_test_data(self) -> None:
        """Setup test data."""
        # Add suppliers
        self.order_processor.add_supplier(1, "Test Supplier", "test@supplier.com", 4.5)
        
        # Add products
        self.order_processor.add_product(1, "Test Product", 99.99, 10, "Electronics", 1.0, 1)
        
        # Add customers
        self.order_processor.add_customer(101, "Test Customer", "test@customer.com", "gold", "555-0123", "123 Test St")
        
        # Add promotions
        future_date = datetime.datetime.now() + datetime.timedelta(days=30)
        self.order_processor.add_promotion(1, "TEST10", 10, 50, future_date, "Electronics")

    def test_save_and_load_data(self) -> None:
        """Test saving and loading data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            filename = temp_file.name

        try:
            # Save data
            result = self.data_loader.save_data_to_file(filename)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(filename))

            # Create new order processor and loader
            new_processor = OrderProcessor()
            new_loader = DataLoaderService(new_processor)

            # Load data
            result = new_loader.load_data_from_file(filename)
            self.assertTrue(result)

            # Verify data was loaded
            product = new_processor.product_service.get_product(1)
            self.assertIsNotNone(product)
            assert product is not None  # Type narrowing for mypy
            self.assertEqual(product.name, "Test Product")

            customer = new_processor.customer_service.get_customer(101)
            self.assertIsNotNone(customer)
            assert customer is not None  # Type narrowing for mypy
            self.assertEqual(customer.name, "Test Customer")

        finally:
            # Cleanup
            if os.path.exists(filename):
                os.unlink(filename)

    def test_export_customers_csv(self) -> None:
        """Test exporting customers to CSV."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            filename = temp_file.name

        try:
            # Export customers
            result = self.data_loader.export_customers_csv(filename)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(filename))

            # Verify CSV content
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn('customer_id,name,email', content)
                self.assertIn('Test Customer', content)

        finally:
            # Cleanup
            if os.path.exists(filename):
                os.unlink(filename)

    def test_get_data_summary(self) -> None:
        """Test getting data summary."""
        summary = self.data_loader.get_data_summary()
        
        self.assertIn('total_products', summary)
        self.assertIn('total_customers', summary)
        self.assertIn('total_orders', summary)
        self.assertIn('low_stock_products', summary)
        
        self.assertEqual(summary['total_products'], 1)
        self.assertEqual(summary['total_customers'], 1)
        self.assertEqual(summary['total_orders'], 0)

    def test_load_nonexistent_file(self) -> None:
        """Test loading from nonexistent file."""
        result = self.data_loader.load_data_from_file('nonexistent.json')
        self.assertFalse(result)

    def test_save_to_invalid_path(self) -> None:
        """Test saving to invalid path."""
        result = self.data_loader.save_data_to_file('/invalid/path/file.json')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()