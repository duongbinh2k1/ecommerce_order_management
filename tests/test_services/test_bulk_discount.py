"""Test cases for BulkDiscountStrategy."""
import unittest
from services.pricing.strategies.bulk_discount import BulkDiscountStrategyImpl


class TestBulkDiscountStrategy(unittest.TestCase):
    """Test cases for BulkDiscountStrategy class."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.strategy = BulkDiscountStrategyImpl()

    def test_bulk_discount_10_or_more_items(self) -> None:
        """Test bulk discount for 10 or more items (5% discount)."""
        # Test exactly 10 items
        discount = self.strategy.calculate_discount(total_items=10, current_subtotal=100.0)
        # 5% of $100 = $5.0
        self.assertEqual(discount, 5.0)

        # Test more than 10 items
        discount = self.strategy.calculate_discount(total_items=15, current_subtotal=100.0)
        self.assertEqual(discount, 5.0)

        # Test much larger quantities
        discount = self.strategy.calculate_discount(total_items=100, current_subtotal=100.0)
        self.assertEqual(discount, 5.0)

    def test_bulk_discount_5_to_9_items(self) -> None:
        """Test bulk discount for 5-9 items (2% discount)."""
        # Test exactly 5 items
        discount = self.strategy.calculate_discount(total_items=5, current_subtotal=100.0)
        # 2% of $100 = $2.0
        self.assertEqual(discount, 2.0)

        # Test 6-9 items
        discount = self.strategy.calculate_discount(total_items=6, current_subtotal=100.0)
        self.assertEqual(discount, 2.0)

        discount = self.strategy.calculate_discount(total_items=7, current_subtotal=100.0)
        self.assertEqual(discount, 2.0)

        discount = self.strategy.calculate_discount(total_items=8, current_subtotal=100.0)
        self.assertEqual(discount, 2.0)

        # Test exactly 9 items (just below the 10 threshold)
        discount = self.strategy.calculate_discount(total_items=9, current_subtotal=100.0)
        self.assertEqual(discount, 2.0)

    def test_bulk_discount_less_than_5_items(self) -> None:
        """Test no bulk discount for less than 5 items."""
        # Test 0 items
        discount = self.strategy.calculate_discount(total_items=0, current_subtotal=100.0)
        self.assertEqual(discount, 0.0)

        # Test 1-4 items
        discount = self.strategy.calculate_discount(total_items=1, current_subtotal=100.0)
        self.assertEqual(discount, 0.0)

        discount = self.strategy.calculate_discount(total_items=2, current_subtotal=100.0)
        self.assertEqual(discount, 0.0)

        discount = self.strategy.calculate_discount(total_items=3, current_subtotal=100.0)
        self.assertEqual(discount, 0.0)

        # Test exactly 4 items (just below the 5 threshold)
        discount = self.strategy.calculate_discount(total_items=4, current_subtotal=100.0)
        self.assertEqual(discount, 0.0)

    def test_bulk_discount_subtotal_parameter_unused(self) -> None:
        """Test that subtotal parameter affects the discount calculation proportionally."""
        # Same quantity, different subtotals should give proportional discount amounts
        discount1 = self.strategy.calculate_discount(total_items=10, current_subtotal=50.0)
        discount2 = self.strategy.calculate_discount(total_items=10, current_subtotal=1000.0)
        discount3 = self.strategy.calculate_discount(total_items=10, current_subtotal=0.0)

        # 5% of $50 = $2.5, 5% of $1000 = $50.0, 5% of $0 = $0.0
        self.assertEqual(discount1, 2.5)
        self.assertEqual(discount2, 50.0)
        self.assertEqual(discount3, 0.0)

    def test_bulk_discount_boundary_values(self) -> None:
        """Test boundary values for bulk discount thresholds."""
        # Test boundary between no discount and 2% discount
        no_discount = self.strategy.calculate_discount(total_items=4, current_subtotal=100.0)
        small_discount = self.strategy.calculate_discount(total_items=5, current_subtotal=100.0)

        self.assertEqual(no_discount, 0.0)
        self.assertEqual(small_discount, 2.0)

        # Test boundary between 2% and 5% discount
        small_discount = self.strategy.calculate_discount(total_items=9, current_subtotal=100.0)
        large_discount = self.strategy.calculate_discount(total_items=10, current_subtotal=100.0)

        self.assertEqual(small_discount, 2.0)
        self.assertEqual(large_discount, 5.0)

    def test_bulk_discount_negative_items(self) -> None:
        """Test bulk discount with negative item count."""
        # Negative items should return no discount
        discount = self.strategy.calculate_discount(total_items=-1, current_subtotal=100.0)
        self.assertEqual(discount, 0.0)

        discount = self.strategy.calculate_discount(total_items=-10, current_subtotal=100.0)
        self.assertEqual(discount, 0.0)


if __name__ == '__main__':
    unittest.main()