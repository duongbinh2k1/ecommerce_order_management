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

    def test_estimate_delivery_time_standard(self) -> None:
        """Test delivery time estimation for standard shipping."""
        time = self.shipping_service.estimate_delivery_time(
            shipping_method=ShippingMethod.STANDARD,
            distance_km=100.0
        )
        
        # Standard: 72 hours base time
        self.assertEqual(time, 72)

    def test_estimate_delivery_time_express_long_distance(self) -> None:
        """Test delivery time estimation for express shipping with long distance."""
        time = self.shipping_service.estimate_delivery_time(
            shipping_method=ShippingMethod.EXPRESS,
            distance_km=600.0
        )
        
        # Express: 24 hours base + 24 hours for long distance = 48
        self.assertEqual(time, 48)

    def test_estimate_delivery_time_overnight(self) -> None:
        """Test delivery time estimation for overnight shipping."""
        time = self.shipping_service.estimate_delivery_time(
            shipping_method=ShippingMethod.OVERNIGHT,
            distance_km=150.0
        )
        
        # Overnight: 12 hours base
        self.assertEqual(time, 12)

    def test_get_available_shipping_methods_light_package(self) -> None:
        """Test available shipping methods for light package."""
        methods = self.shipping_service.get_available_shipping_methods(weight=5.0)
        
        # All methods should be available for light package
        expected_methods = [
            ShippingMethod.STANDARD,
            ShippingMethod.EXPRESS,
            ShippingMethod.OVERNIGHT
        ]
        self.assertEqual(set(methods), set(expected_methods))

    def test_get_available_shipping_methods_medium_package(self) -> None:
        """Test available shipping methods for medium package."""
        methods = self.shipping_service.get_available_shipping_methods(weight=15.0)
        
        # Only standard and express available
        expected_methods = [
            ShippingMethod.STANDARD,
            ShippingMethod.EXPRESS
        ]
        self.assertEqual(set(methods), set(expected_methods))

    def test_get_available_shipping_methods_heavy_package(self) -> None:
        """Test available shipping methods for heavy package."""
        methods = self.shipping_service.get_available_shipping_methods(weight=25.0)
        
        # Only standard available
        expected_methods = [ShippingMethod.STANDARD]
        self.assertEqual(methods, expected_methods)

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


if __name__ == '__main__':
    unittest.main()