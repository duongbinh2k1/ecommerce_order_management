"""
Test Product domain model - validation and business rules
Tests the refactored Product class business logic
"""
import unittest
from domain.models.product import Product
from domain.enums.product_category import ProductCategory


class TestProduct(unittest.TestCase):
    """Test Product domain model validation and business rules."""

    def test_product_creation_valid(self) -> None:
        """Test creating Product with valid data."""
        product = Product(
            product_id=1,
            name="Test Product",
            price=99.99,
            quantity_available=10,
            category="Electronics",
            weight=1.5,
            supplier_id=1
        )
        
        self.assertEqual(product.product_id, 1)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price.value, 99.99)
        self.assertEqual(product.quantity_available, 10)
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.weight, 1.5)
        self.assertEqual(product.supplier_id, 1)

    def test_product_validation_invalid_price(self) -> None:
        """Test Product validation - should reject negative price."""
        with self.assertRaises(ValueError):
            Product(
                product_id=1,
                name="Test Product",
                price=-10.0,  # Invalid negative price
                quantity_available=10,
                category="Electronics",
                weight=1.5,
                supplier_id=1
            )

    def test_product_validation_invalid_quantity(self) -> None:
        """Test Product validation - should reject negative quantity."""
        with self.assertRaises(ValueError):
            Product(
                product_id=1,
                name="Test Product",
                price=99.99,
                quantity_available=-5,  # Invalid negative quantity
                category="Electronics",
                weight=1.5,
                supplier_id=1
            )

    def test_product_validation_invalid_weight(self) -> None:
        """Test Product validation - should reject negative weight."""
        with self.assertRaises(ValueError):
            Product(
                product_id=1,
                name="Test Product",
                price=99.99,
                quantity_available=10,
                category="Electronics",
                weight=-1.0,  # Invalid negative weight
                supplier_id=1
            )

    def test_product_validation_empty_name(self) -> None:
        """Test Product validation - should reject empty name."""
        with self.assertRaises(ValueError):
            Product(
                product_id=1,
                name="",  # Invalid empty name
                price=99.99,
                quantity_available=10,
                category="Electronics",
                weight=1.5,
                supplier_id=1
            )

    def test_product_validation_category_edge_cases(self) -> None:
        """Test Product validation - test invalid category inputs."""
        # Empty category should raise ValueError now that we use enum
        with self.assertRaises(ValueError):
            Product(
                product_id=1,
                name="Test Product",
                price=99.99,
                quantity_available=10,
                category="",  # Invalid - empty string not in enum
                weight=1.5,
                supplier_id=1
            )

        # Invalid category should also raise ValueError
        with self.assertRaises(ValueError):
            Product(
                product_id=2,
                name="Test Product 2",
                price=99.99,
                quantity_available=10,
                category="InvalidCategory",  # Invalid - not in enum
                weight=1.5,
                supplier_id=1
            )

        # Valid category should work fine
        valid_product = Product(
            product_id=3,
            name="Valid Product",
            price=99.99,
            quantity_available=10,
            category=ProductCategory.ELECTRONICS,  # Valid enum value
            weight=1.5,
            supplier_id=1
        )
        self.assertEqual(valid_product.category, ProductCategory.ELECTRONICS)

    def test_product_availability_check(self) -> None:
        """Test Product availability based on quantity."""
        # Product with stock
        product1 = Product(
            product_id=1,
            name="Test Product",
            price=99.99,
            quantity_available=10,
            category="Electronics",
            weight=1.5,
            supplier_id=1
        )
        self.assertGreater(product1.quantity_available, 0)
        
        # Product without stock
        product2 = Product(
            product_id=2,
            name="Out of Stock Product",
            price=99.99,
            quantity_available=0,
            category="Electronics",
            weight=1.5,
            supplier_id=1
        )
        self.assertEqual(product2.quantity_available, 0)

    def test_product_object_creation(self) -> None:
        """Test Product object creation and basic properties."""
        product = Product(
            product_id=1,
            name="Test Product",
            price=99.99,
            quantity_available=10,
            category="Electronics",
            weight=1.5,
            supplier_id=1
        )
        
        # Test that object is created successfully
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.product_id, 1)


if __name__ == '__main__':
    unittest.main()