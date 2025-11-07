"""Test cases for ShippingService."""
import unittest
from unittest.mock import Mock
from services.shipping_service import ShippingService
from domain.enums.shipping_method import ShippingMethod
from domain.enums.membership_tier import MembershipTier


class TestShippingService(unittest.TestCase):
    """Test cases for ShippingService class."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.shipment_repository = Mock()
        self.shipment_repository.get_next_id.return_value = 1
        
        self.shipping_service = ShippingService(self.shipment_repository)

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

    def test_create_shipment_string_method(self) -> None:
        """Test creating shipment with enum shipping method."""
        tracking = self.shipping_service.create_shipment(
            order_id=123,
            shipping_method=ShippingMethod.EXPRESS,  # Use enum
            address="123 Main St"
        )
        
        self.assertTrue(tracking.startswith("TRACK123"))
        self.shipment_repository.add.assert_called_once()
        
        # Verify shipment data
        call_args = self.shipment_repository.add.call_args[0][0]
        self.assertEqual(call_args['order_id'], 123)
        self.assertEqual(call_args['shipping_method'], ShippingMethod.EXPRESS.value)
        self.assertEqual(call_args['address'], "123 Main St")
        self.assertEqual(call_args['status'], 'pending')

    def test_create_shipment_enum_method(self) -> None:
        """Test creating shipment with enum shipping method."""
        tracking = self.shipping_service.create_shipment(
            order_id=456,
            shipping_method=ShippingMethod.STANDARD,
            address="456 Oak Ave"
        )
        
        self.assertTrue(tracking.startswith("TRACK456"))
        self.shipment_repository.add.assert_called_once()
        
        # Verify shipment data
        call_args = self.shipment_repository.add.call_args[0][0]
        self.assertEqual(call_args['shipping_method'], "standard")

    def test_update_shipment_status_success(self) -> None:
        """Test updating shipment status successfully."""
        # Mock existing shipment
        existing_shipment = {
            'shipment_id': 1,
            'tracking_number': 'TRACK123',
            'status': 'pending'
        }
        
        self.shipment_repository.get_all.return_value = {1: existing_shipment}
        
        result = self.shipping_service.update_shipment_status('TRACK123', 'in_transit')
        
        self.assertTrue(result)
        self.assertEqual(existing_shipment['status'], 'in_transit')
        self.shipment_repository.update.assert_called_once_with(existing_shipment)

    def test_update_shipment_status_not_found(self) -> None:
        """Test updating shipment status when tracking number not found."""
        self.shipment_repository.get_all.return_value = {}
        
        result = self.shipping_service.update_shipment_status('NOTFOUND', 'delivered')
        
        self.assertFalse(result)
        self.shipment_repository.update.assert_not_called()

    def test_update_shipment_status_multiple_shipments(self) -> None:
        """Test updating status with multiple shipments."""
        shipments = {
            1: {'tracking_number': 'TRACK111', 'status': 'pending'},
            2: {'tracking_number': 'TRACK222', 'status': 'in_transit'},
            3: {'tracking_number': 'TRACK333', 'status': 'delivered'}
        }
        
        self.shipment_repository.get_all.return_value = shipments
        
        result = self.shipping_service.update_shipment_status('TRACK222', 'delivered')
        
        self.assertTrue(result)
        self.assertEqual(shipments[2]['status'], 'delivered')
        # Other shipments should remain unchanged
        self.assertEqual(shipments[1]['status'], 'pending')
        self.assertEqual(shipments[3]['status'], 'delivered')

    def test_get_tracking_info_found(self) -> None:
        """Test getting tracking info when shipment exists."""
        shipment = {
            'shipment_id': 1,
            'tracking_number': 'TRACK123',
            'order_id': '456',
            'status': 'in_transit',
            'address': '123 Main St'
        }
        
        self.shipment_repository.get_all.return_value = {1: shipment}
        
        result = self.shipping_service.get_tracking_info('TRACK123')
        
        self.assertEqual(result, shipment)

    def test_get_tracking_info_not_found(self) -> None:
        """Test getting tracking info when shipment doesn't exist."""
        self.shipment_repository.get_all.return_value = {}
        
        result = self.shipping_service.get_tracking_info('NOTFOUND')
        
        self.assertEqual(result, {})

    def test_get_tracking_info_multiple_shipments(self) -> None:
        """Test getting specific tracking info from multiple shipments."""
        shipments = {
            1: {'tracking_number': 'TRACK111', 'status': 'pending'},
            2: {'tracking_number': 'TRACK222', 'status': 'delivered'},
            3: {'tracking_number': 'TRACK333', 'status': 'in_transit'}
        }
        
        self.shipment_repository.get_all.return_value = shipments
        
        result = self.shipping_service.get_tracking_info('TRACK333')
        
        self.assertEqual(result, shipments[3])

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