"""
Test PromotionalDiscountStrategy - promotional code discount calculation
Tests promotional discount calculation with various conditions
"""
import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta
from services.pricing.strategies.promotional_discount import PromotionalDiscountStrategy


class TestPromotionalDiscountStrategy(unittest.TestCase):
    """Test PromotionalDiscountStrategy discount calculation."""

    def setUp(self):
        """Set up test dependencies."""
        self.strategy = PromotionalDiscountStrategy()

        # Create mock promotion
        future_date = datetime.now() + timedelta(days=30)
        self.promotion = Mock()
        self.promotion.valid_until = future_date
        self.promotion.min_purchase = Mock()
        self.promotion.min_purchase.value = 100.0
        self.promotion.discount_percent = 20.0
        self.promotion.category = "all"

        # Create mock order items
        self.order_item1 = Mock()
        self.order_item1.product_id = "prod_001"
        
        self.order_item2 = Mock()
        self.order_item2.product_id = "prod_002"

        # Create mock products
        self.product1 = Mock()
        self.product1.category = "electronics"
        
        self.product2 = Mock()
        self.product2.category = "books"

        self.products = {
            "prod_001": self.product1,
            "prod_002": self.product2
        }

    def test_calculate_discount_no_promotion(self):
        """Test discount calculation with no promotion."""
        discount = self.strategy.calculate_discount(
            None, 150.0, [self.order_item1], self.products
        )
        
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_valid_promotion_all_category(self):
        """Test discount calculation with valid promotion for all categories."""
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1], self.products
        )
        
        # 20% of $150 = $30
        self.assertEqual(discount, 30.0)

    def test_calculate_discount_expired_promotion(self):
        """Test discount calculation with expired promotion."""
        past_date = datetime.now() - timedelta(days=5)
        self.promotion.valid_until = past_date
        
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1], self.products
        )
        
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_below_minimum_purchase(self):
        """Test discount calculation below minimum purchase amount."""
        discount = self.strategy.calculate_discount(
            self.promotion, 50.0, [self.order_item1], self.products
        )
        
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_exact_minimum_purchase(self):
        """Test discount calculation at exact minimum purchase amount."""
        discount = self.strategy.calculate_discount(
            self.promotion, 100.0, [self.order_item1], self.products
        )
        
        # 20% of $100 = $20
        self.assertEqual(discount, 20.0)

    def test_calculate_discount_specific_category_match(self):
        """Test discount calculation with specific category match."""
        self.promotion.category = "electronics"
        
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1], self.products
        )
        
        # Product 1 is in electronics category, so discount applies
        self.assertEqual(discount, 30.0)

    def test_calculate_discount_specific_category_no_match(self):
        """Test discount calculation with specific category no match."""
        self.promotion.category = "clothing"
        
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1, self.order_item2], self.products
        )
        
        # No products match clothing category
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_mixed_categories_partial_match(self):
        """Test discount calculation with mixed categories, partial match."""
        self.promotion.category = "electronics"
        
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1, self.order_item2], self.products
        )
        
        # Only product 1 matches electronics, but discount applies to entire order
        self.assertEqual(discount, 30.0)

    def test_calculate_discount_product_not_found(self):
        """Test discount calculation when product not found."""
        self.order_item1.product_id = "nonexistent"
        
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1], self.products
        )
        
        # Product not found, so no match for category
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_empty_order_items(self):
        """Test discount calculation with empty order items."""
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [], self.products
        )
        
        # No items to check category against
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_high_percentage(self):
        """Test discount calculation with high percentage."""
        self.promotion.discount_percent = 50.0
        
        discount = self.strategy.calculate_discount(
            self.promotion, 200.0, [self.order_item1], self.products
        )
        
        # 50% of $200 = $100
        self.assertEqual(discount, 100.0)

    def test_calculate_discount_zero_percentage(self):
        """Test discount calculation with zero percentage."""
        self.promotion.discount_percent = 0.0
        
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1], self.products
        )
        
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_small_subtotal(self):
        """Test discount calculation with small subtotal."""
        self.promotion.min_purchase.value = 10.0
        
        discount = self.strategy.calculate_discount(
            self.promotion, 15.0, [self.order_item1], self.products
        )
        
        # 20% of $15 = $3
        self.assertEqual(discount, 3.0)

    def test_calculate_discount_category_case_sensitivity(self):
        """Test discount calculation with case-sensitive category matching."""
        self.promotion.category = "Electronics"  # Capital E
        self.product1.category = "electronics"   # lowercase e
        
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1], self.products
        )
        
        # Should not match due to case sensitivity
        self.assertEqual(discount, 0.0)

    def test_calculate_discount_just_expired(self):
        """Test discount calculation with promotion that just expired."""
        just_expired = datetime.now() - timedelta(microseconds=1)
        self.promotion.valid_until = just_expired
        
        discount = self.strategy.calculate_discount(
            self.promotion, 150.0, [self.order_item1], self.products
        )
        
        self.assertEqual(discount, 0.0)


if __name__ == '__main__':
    unittest.main()