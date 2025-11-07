"""
Test Money value object - validation and arithmetic operations
Tests the refactored Money class from domain layer
"""
import unittest
from domain.value_objects.money import Money


class TestMoney(unittest.TestCase):
    """Test Money value object validation and operations."""

    def test_money_creation_valid(self) -> None:
        """Test creating Money with valid amounts."""
        # Test with integer
        money1 = Money(100)
        self.assertEqual(money1.value, 100.0)
        
        # Test with float
        money2 = Money(99.99)
        self.assertEqual(money2.value, 99.99)
        
        # Test with zero
        money3 = Money(0)
        self.assertEqual(money3.value, 0.0)

    def test_money_creation_edge_cases(self) -> None:
        """Test Money creation with edge cases."""
        # Test with negative amount (currently allowed in implementation)
        money_negative = Money(-1)
        self.assertEqual(money_negative.value, -1.0)
        
        # Test with very small amount
        money_small = Money(0.01)
        self.assertEqual(money_small.value, 0.01)

    def test_money_arithmetic_operations(self) -> None:
        """Test Money arithmetic operations."""
        money1 = Money(100)
        money2 = Money(50)
        
        # Addition
        result_add = money1 + money2
        self.assertEqual(result_add.value, 150.0)
        
        # Addition with number
        result_add_num = money1 + 25
        self.assertEqual(result_add_num.value, 125.0)
        
        # Subtraction
        result_sub = money1 - money2
        self.assertEqual(result_sub.value, 50.0)
        
        # Subtraction with number
        result_sub_num = money1 - 25
        self.assertEqual(result_sub_num.value, 75.0)
        
        # Multiplication
        result_mul = money1 * 2
        self.assertEqual(result_mul.value, 200.0)
        
        # Division
        result_div = money1 / 2
        self.assertEqual(result_div.value, 50.0)

    def test_money_comparison_operations(self) -> None:
        """Test Money comparison operations."""
        money1 = Money(100)
        money2 = Money(50)
        money3 = Money(100)
        
        # Less than
        self.assertTrue(money2 < money1)
        self.assertFalse(money1 < money2)
        
        # Less than or equal
        self.assertTrue(money2 <= money1)
        self.assertTrue(money1 <= money3)
        
        # Greater than
        self.assertTrue(money1 > money2)
        self.assertFalse(money2 > money1)
        
        # Greater than or equal
        self.assertTrue(money1 >= money2)
        self.assertTrue(money1 >= money3)
        
        # Equality
        self.assertTrue(money1 == money3)
        self.assertFalse(money1 == money2)

    def test_money_string_representation(self) -> None:
        """Test Money string representation."""
        money = Money(99.99)
        self.assertEqual(str(money), "$99.99")  # Match actual implementation
        self.assertEqual(repr(money), "Money(99.99)")


if __name__ == '__main__':
    unittest.main()