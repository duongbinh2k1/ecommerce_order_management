"""
Test LoyaltyPointsDiscountStrategy - loyalty points discount calculation
Tests loyalty points discount calculation and usage
"""
import unittest
from services.pricing.strategies.loyalty_discount import LoyaltyDiscountStrategyImpl


class TestLoyaltyPointsDiscountStrategy(unittest.TestCase):
    """Test LoyaltyPointsDiscountStrategy discount calculation."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.strategy = LoyaltyDiscountStrategyImpl()

    def test_calculate_discount_insufficient_points(self) -> None:
        """Test discount calculation with insufficient points."""
        discount = self.strategy.calculate_discount(loyalty_points=50, current_subtotal=100.0)
        points_used = self.strategy.calculate_points_used(discount)
        
        self.assertEqual(discount, 0.0)
        self.assertEqual(points_used, 0)

    def test_calculate_discount_minimum_points(self) -> None:
        """Test discount calculation with minimum required points."""
        discount = self.strategy.calculate_discount(loyalty_points=100, current_subtotal=100.0)
        points_used = self.strategy.calculate_points_used(discount)
        
        self.assertEqual(discount, 1.0)  # 100 points * 0.01 = $1
        self.assertEqual(points_used, 100)

    def test_calculate_discount_within_limit(self) -> None:
        """Test discount calculation within 10% limit."""
        discount = self.strategy.calculate_discount(loyalty_points=500, current_subtotal=100.0)
        points_used = self.strategy.calculate_points_used(discount)
        
        # 500 points * 0.01 = $5 discount
        # Max 10% of $100 = $10, so $5 is allowed
        self.assertEqual(discount, 5.0)
        self.assertEqual(points_used, 500)

    def test_calculate_discount_exceeds_limit(self) -> None:
        """Test discount calculation that exceeds 10% limit."""
        discount = self.strategy.calculate_discount(loyalty_points=2000, current_subtotal=100.0)
        points_used = self.strategy.calculate_points_used(discount)
        
        # 2000 points * 0.01 = $20 discount
        # Max 10% of $100 = $10, so capped at $10
        self.assertEqual(discount, 10.0)  # Capped at 10% of subtotal
        self.assertEqual(points_used, 1000)  # $10 * 100 = 1000 points

    def test_calculate_discount_large_subtotal(self) -> None:
        """Test discount calculation with large subtotal."""
        discount = self.strategy.calculate_discount(loyalty_points=1500, current_subtotal=500.0)
        points_used = self.strategy.calculate_points_used(discount)
        
        # 1500 points * 0.01 = $15 discount
        # Max 10% of $500 = $50, so $15 is allowed
        self.assertEqual(discount, 15.0)
        self.assertEqual(points_used, 1500)

    def test_calculate_discount_exact_limit(self) -> None:
        """Test discount calculation at exactly 10% limit."""
        discount = self.strategy.calculate_discount(loyalty_points=1000, current_subtotal=100.0)
        points_used = self.strategy.calculate_points_used(discount)
        
        # 1000 points * 0.01 = $10 discount
        # Max 10% of $100 = $10, exactly at limit
        self.assertEqual(discount, 10.0)
        self.assertEqual(points_used, 1000)

    def test_calculate_discount_zero_subtotal(self) -> None:
        """Test discount calculation with zero subtotal."""
        discount = self.strategy.calculate_discount(loyalty_points=500, current_subtotal=0.0)
        points_used = self.strategy.calculate_points_used(discount)
        
        # Max discount is 10% of $0 = $0
        self.assertEqual(discount, 0.0)
        self.assertEqual(points_used, 0)

    def test_calculate_discount_small_subtotal(self) -> None:
        """Test discount calculation with small subtotal."""
        discount = self.strategy.calculate_discount(loyalty_points=1000, current_subtotal=10.0)
        points_used = self.strategy.calculate_points_used(discount)
        
        # 1000 points * 0.01 = $10 discount
        # Max 10% of $10 = $1, so capped at $1
        self.assertEqual(discount, 1.0)
        self.assertEqual(points_used, 100)  # $1 * 100 = 100 points

    def test_calculate_discount_boundary_cases(self) -> None:
        """Test discount calculation boundary cases."""
        # Just below minimum points
        discount1 = self.strategy.calculate_discount(loyalty_points=99, current_subtotal=100.0)
        points_used1 = self.strategy.calculate_points_used(discount1)
        self.assertEqual(discount1, 0.0)
        self.assertEqual(points_used1, 0)
        
        # Just at minimum points
        discount2 = self.strategy.calculate_discount(loyalty_points=100, current_subtotal=100.0)
        points_used2 = self.strategy.calculate_points_used(discount2)
        self.assertEqual(discount2, 1.0)
        self.assertEqual(points_used2, 100)

    def test_calculate_discount_float_precision(self) -> None:
        """Test discount calculation with float precision."""
        discount = self.strategy.calculate_discount(loyalty_points=150, current_subtotal=33.33)
        points_used = self.strategy.calculate_points_used(discount)
        
        # 150 points * 0.01 = $1.5 discount
        # Max 10% of $33.33 = $3.333, so $1.5 is allowed
        self.assertEqual(discount, 1.5)
        self.assertEqual(points_used, 150)


if __name__ == '__main__':
    unittest.main()