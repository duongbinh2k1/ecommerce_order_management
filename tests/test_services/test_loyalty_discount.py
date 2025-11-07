"""
Test LoyaltyPointsDiscountStrategy - loyalty points discount calculation
Tests loyalty points discount calculation and usage
"""
import unittest
from services.pricing.strategies.loyalty_discount import LoyaltyPointsDiscountStrategy


class TestLoyaltyPointsDiscountStrategy(unittest.TestCase):
    """Test LoyaltyPointsDiscountStrategy discount calculation."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.strategy = LoyaltyPointsDiscountStrategy()

    def test_calculate_discount_insufficient_points(self) -> None:
        """Test discount calculation with insufficient points."""
        discount, points_used = self.strategy.calculate_discount(50, 100.0)
        
        self.assertEqual(discount, 0.0)
        self.assertEqual(points_used, 0)

    def test_calculate_discount_minimum_points(self) -> None:
        """Test discount calculation with minimum required points."""
        discount, points_used = self.strategy.calculate_discount(100, 100.0)
        
        self.assertEqual(discount, 1.0)  # 100 points * 0.01 = $1
        self.assertEqual(points_used, 100)

    def test_calculate_discount_within_limit(self) -> None:
        """Test discount calculation within 10% limit."""
        discount, points_used = self.strategy.calculate_discount(500, 100.0)
        
        # 500 points * 0.01 = $5 discount
        # Max 10% of $100 = $10, so $5 is allowed
        self.assertEqual(discount, 5.0)
        self.assertEqual(points_used, 500)

    def test_calculate_discount_exceeds_limit(self) -> None:
        """Test discount calculation that exceeds 10% limit."""
        discount, points_used = self.strategy.calculate_discount(2000, 100.0)
        
        # 2000 points * 0.01 = $20 discount
        # Max 10% of $100 = $10, so capped at $10
        self.assertEqual(discount, 10.0)  # Capped at 10% of subtotal
        self.assertEqual(points_used, 1000)  # $10 * 100 = 1000 points

    def test_calculate_discount_large_subtotal(self) -> None:
        """Test discount calculation with large subtotal."""
        discount, points_used = self.strategy.calculate_discount(1500, 500.0)
        
        # 1500 points * 0.01 = $15 discount
        # Max 10% of $500 = $50, so $15 is allowed
        self.assertEqual(discount, 15.0)
        self.assertEqual(points_used, 1500)

    def test_calculate_discount_exact_limit(self) -> None:
        """Test discount calculation at exactly 10% limit."""
        discount, points_used = self.strategy.calculate_discount(1000, 100.0)
        
        # 1000 points * 0.01 = $10 discount
        # Max 10% of $100 = $10, exactly at limit
        self.assertEqual(discount, 10.0)
        self.assertEqual(points_used, 1000)

    def test_calculate_discount_zero_subtotal(self) -> None:
        """Test discount calculation with zero subtotal."""
        discount, points_used = self.strategy.calculate_discount(500, 0.0)
        
        # Max discount is 10% of $0 = $0
        self.assertEqual(discount, 0.0)
        self.assertEqual(points_used, 0)

    def test_calculate_discount_small_subtotal(self) -> None:
        """Test discount calculation with small subtotal."""
        discount, points_used = self.strategy.calculate_discount(1000, 10.0)
        
        # 1000 points * 0.01 = $10 discount
        # Max 10% of $10 = $1, so capped at $1
        self.assertEqual(discount, 1.0)
        self.assertEqual(points_used, 100)  # $1 * 100 = 100 points

    def test_calculate_discount_boundary_cases(self) -> None:
        """Test discount calculation boundary cases."""
        # Just below minimum points
        discount1, points_used1 = self.strategy.calculate_discount(99, 100.0)
        self.assertEqual(discount1, 0.0)
        self.assertEqual(points_used1, 0)
        
        # Just at minimum points
        discount2, points_used2 = self.strategy.calculate_discount(100, 100.0)
        self.assertEqual(discount2, 1.0)
        self.assertEqual(points_used2, 100)

    def test_calculate_discount_float_precision(self) -> None:
        """Test discount calculation with float precision."""
        discount, points_used = self.strategy.calculate_discount(150, 33.33)
        
        # 150 points * 0.01 = $1.5 discount
        # Max 10% of $33.33 = $3.333, so $1.5 is allowed
        self.assertEqual(discount, 1.5)
        self.assertEqual(points_used, 150)


if __name__ == '__main__':
    unittest.main()