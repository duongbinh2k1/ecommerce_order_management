"""
Test ProductService - with mocked repository dependencies
Tests the refactored ProductService business logic in isolation
"""
import unittest
from unittest.mock import Mock
from services.product_service import ProductService
from domain.models.product import Product


class TestProductService(unittest.TestCase):
    """Test ProductService with mocked repository dependencies."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        # Mock repository
        self.mock_repository = Mock()
        
        # Create service with mocked repository
        self.product_service = ProductService(self.mock_repository)

    def test_add_product_success(self) -> None:
        """Test adding a product successfully."""
        # Test adding a product
        product = self.product_service.add_product(
            product_id=1,  # Changed from string to int
            name="Test Product",
            price=99.99,
            quantity=10,
            category="Electronics",
            weight=1.5,
            supplier_id=1  # Changed from string to int
        )
        
        # Verify product was created correctly
        self.assertEqual(product.product_id, 1)  # product_id is int, not string
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price.value, 99.99)
        
        # Verify repository.add was called
        self.mock_repository.add.assert_called_once_with(product)

    def test_get_product_found(self) -> None:
        """Test getting a product that exists."""
        # Mock repository return
        expected_product = Product(
            product_id=1,
            name="Test Product",
            price=99.99,
            quantity_available=10,
            category="Electronics",
            weight=1.5,
            supplier_id=1
        )
        self.mock_repository.get.return_value = expected_product
        
        # Get product
        result = self.product_service.get_product(1)
        
        # Verify result
        self.assertEqual(result, expected_product)
        self.mock_repository.get.assert_called_once_with(1)

    def test_get_product_not_found(self) -> None:
        """Test getting a product that doesn't exist."""
        # Mock repository return None
        self.mock_repository.get.return_value = None
        
        # Get product
        result = self.product_service.get_product(999)
        
        # Verify result
        self.assertIsNone(result)
        self.mock_repository.get.assert_called_once_with(999)

    def test_update_product_price_success(self) -> None:
        """Test updating a product price successfully."""
        # Mock existing product
        existing_product = Product(
            product_id=1,
            name="Test Product",
            price=99.99,
            quantity_available=10,
            category="Electronics",
            weight=1.5,
            supplier_id=1
        )
        self.mock_repository.get.return_value = existing_product
        
        # Update product price
        result = self.product_service.update_product_price(1, 199.99)
        
        # Verify result and repository calls
        self.assertTrue(result)
        self.mock_repository.get.assert_called_once_with(1)
        self.mock_repository.update.assert_called_once()

    def test_update_product_quantity_success(self) -> None:
        """Test updating a product quantity successfully."""
        # Mock existing product
        existing_product = Product(
            product_id=1,
            name="Test Product",
            price=99.99,
            quantity_available=10,
            category="Electronics",
            weight=1.5,
            supplier_id=1
        )
        self.mock_repository.get.return_value = existing_product
        
        # Update product quantity
        result = self.product_service.update_product_quantity(1, 20)
        
        # Verify result and repository calls
        self.assertTrue(result)
        self.mock_repository.get.assert_called_once_with(1)
        self.mock_repository.update.assert_called_once()

    def test_get_all_products(self) -> None:
        """Test getting all products."""
        # Mock repository return
        expected_products = {
            1: Product(1, "Product 1", 99.99, 10, "Electronics", 1.0, 1),
            2: Product(2, "Product 2", 199.99, 5, "Electronics", 2.0, 2)
        }
        self.mock_repository.get_all.return_value = expected_products
        
        # Get all products
        result = self.product_service.get_all_products()
        
        # Verify result
        self.assertEqual(result, expected_products)
        self.mock_repository.get_all.assert_called_once()


if __name__ == '__main__':
    unittest.main()