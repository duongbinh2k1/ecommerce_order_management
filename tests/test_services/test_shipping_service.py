"""Test cases for ShippingService."""
import unittest
from services.shipping_service import ShippingService
from domain.enums.shipping_method import ShippingMethod
from domain.enums.membership_tier import MembershipTier


class TestShippingService(unittest.TestCase):
    """Test cases for ShippingService class."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.shipping_service = ShippingService()

    def test_calculate_shipping_cost_express_gold(self) -> None:
        """Test express shipping cost for gold member."""
        cost = self.shipping_service.calculate_shipping_cost(
            shipping_method=ShippingMethod.EXPRESS,
            total_weight=2.0,
            subtotal=100.0,
            customer_tier=MembershipTier.GOLD
        )
        
        # Express: 25 + (2.0 * 0.5) = 26, Gold gets 50% off = 13
        expected_cost = (25 + (2.0 * 0.5)) * 0.5
        self.assertEqual(cost, expected_cost)

    def test_calculate_shipping_cost_express_standard(self) -> None:
        """Test express shipping cost for standard member."""
        cost = self.shipping_service.calculate_shipping_cost(
            shipping_method=ShippingMethod.EXPRESS,
            total_weight=1.5,
            subtotal=100.0,
            customer_tier=MembershipTier.STANDARD
        )
        
        # Express: 25 + (1.5 * 0.5) = 25.75
        expected_cost = 25 + (1.5 * 0.5)
        self.assertEqual(cost, expected_cost)

    def test_calculate_shipping_cost_standard_under_threshold(self) -> None:
        """Test standard shipping cost under free shipping threshold."""
        cost = self.shipping_service.calculate_shipping_cost(
            shipping_method=ShippingMethod.STANDARD,
            total_weight=1.0,
            subtotal=30.0,  # Under $50
            customer_tier=MembershipTier.STANDARD
        )
        
        # Standard under $50: 5 + (1.0 * 0.2) = 5.2
        expected_cost = 5 + (1.0 * 0.2)
        self.assertEqual(cost, expected_cost)

    def test_calculate_shipping_cost_standard_free_shipping(self) -> None:
        """Test standard shipping cost over free shipping threshold."""
        cost = self.shipping_service.calculate_shipping_cost(
            shipping_method=ShippingMethod.STANDARD,
            total_weight=2.0,
            subtotal=75.0,  # Over $50
            customer_tier=MembershipTier.BRONZE
        )
        
        # Standard over $50: free shipping
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_cost_overnight(self) -> None:
        """Test overnight shipping cost."""
        cost = self.shipping_service.calculate_shipping_cost(
            shipping_method=ShippingMethod.OVERNIGHT,
            total_weight=3.0,
            subtotal=200.0,
            customer_tier=MembershipTier.SILVER
        )
        
        # Overnight: 50 + (3.0 * 1.0) = 53
        expected_cost = 50 + (3.0 * 1.0)
        self.assertEqual(cost, expected_cost)

    def test_calculate_shipping_cost_zero_weight(self) -> None:
        """Test shipping cost calculation with zero weight."""
        cost = self.shipping_service.calculate_shipping_cost(
            shipping_method=ShippingMethod.EXPRESS,
            total_weight=0.0,
            subtotal=100.0,
            customer_tier=MembershipTier.STANDARD
        )
        
        # Express: 25 + (0.0 * 0.5) = 25
        self.assertEqual(cost, 25.0)

    def test_calculate_shipping_cost_high_weight(self) -> None:
        """Test shipping cost calculation with high weight."""
        cost = self.shipping_service.calculate_shipping_cost(
            shipping_method=ShippingMethod.OVERNIGHT,
            total_weight=50.0,
            subtotal=1000.0,
            customer_tier=MembershipTier.GOLD
        )
        
        # Overnight: 50 + (50.0 * 1.0) = 100, no gold discount for overnight
        self.assertEqual(cost, 100.0)

    def test_calculate_shipping_cost_standard_exactly_threshold(self) -> None:
        """Test standard shipping cost at exactly $50 threshold."""
        cost = self.shipping_service.calculate_shipping_cost(
            shipping_method=ShippingMethod.STANDARD,
            total_weight=2.5,
            subtotal=50.0,  # Exactly $50
            customer_tier=MembershipTier.SILVER
        )
        
        # Standard at $50: free shipping
        self.assertEqual(cost, 0.0)


if __name__ == '__main__':
    unittest.main()