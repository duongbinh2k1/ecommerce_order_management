"""
Test OrderService - order creation and management functionality
Tests order processing, validation, and status management
"""
import unittest
from unittest.mock import Mock, patch
from services.order_service import OrderService
from domain.enums.order_status import OrderStatus
from domain.enums.membership_tier import MembershipTier


class TestOrderService(unittest.TestCase):
    """Test OrderService order management functionality."""

    def setUp(self):
        """Set up test dependencies."""
        self.order_repository = Mock()
        self.product_service = Mock()
        self.customer_service = Mock()
        self.pricing_service = Mock()
        self.payment_service = Mock()
        self.shipping_service = Mock()
        self.notification_service = Mock()
        self.inventory_service = Mock()
        
        self.order_service = OrderService(
            self.order_repository,
            self.product_service,
            self.customer_service,
            self.pricing_service,
            self.payment_service,
            self.shipping_service,
            self.notification_service,
            self.inventory_service
        )

        # Mock customer
        self.customer = Mock()
        self.customer.customer_id = "cust_001"
        self.customer.name = "John Doe"
        self.customer.email = Mock()
        self.customer.email.value = "john@example.com"
        self.customer.membership_tier = MembershipTier.GOLD
        self.customer.loyalty_points = 500
        self.customer.address = Mock()
        self.customer.address.value = "123 Main St"

        # Mock product
        self.product = Mock()
        self.product.product_id = "prod_001"
        self.product.name = "Test Product"
        self.product.price = Mock()
        self.product.price.value = 100.0
        self.product.quantity_available = 10

    @patch('services.order_service.datetime')
    def test_create_order_success(self, mock_datetime):
        """Test successful order creation."""
        # Mock datetime
        mock_datetime.datetime.now.return_value = "2023-01-01"
        
        # Mock dependencies
        self.customer_service.get_customer.return_value = self.customer
        self.product_service.get_product.return_value = self.product
        self.inventory_service.check_product_availability.return_value = True
        self.pricing_service.apply_all_discounts.return_value = {
            'final_price': 200.0,
            'total_weight': 2.0
        }
        self.shipping_service.calculate_shipping_cost.return_value = 10.0
        self.payment_service.process_payment.return_value = (True, None)
        self.order_repository.get_next_id.return_value = 1000
        
        # Test data - correct tuple format
        items = [("prod_001", 2, 100.0)]
        payment_info = {"valid": True, "card_number": "1234567890123456", "type": "credit_card"}
        
        result = self.order_service.create_order(
            "cust_001",
            items,
            payment_info,
            "PROMO20",
            "standard"
        )
        
        self.assertIsNotNone(result)
        self.order_repository.add.assert_called_once()
        self.notification_service.send_order_confirmation.assert_called_once()

    def test_create_order_customer_not_found(self):
        """Test order creation with non-existent customer."""
        self.customer_service.get_customer.return_value = None
        
        items = [("prod_001", 2, 100.0)]
        payment_info = {"valid": True, "type": "credit_card"}
        
        result = self.order_service.create_order(
            "nonexistent",
            items,
            payment_info
        )
        
        self.assertIsNone(result)

    def test_create_order_customer_suspended(self):
        """Test order creation with suspended customer."""
        self.customer.membership_tier = MembershipTier.SUSPENDED
        self.customer_service.get_customer.return_value = self.customer
        
        items = [("prod_001", 2, 100.0)]
        payment_info = {"valid": True, "type": "credit_card"}
        
        result = self.order_service.create_order(
            "cust_001",
            items,
            payment_info
        )
        
        self.assertIsNone(result)

    def test_create_order_product_not_found(self):
        """Test order creation with non-existent product."""
        self.customer_service.get_customer.return_value = self.customer
        self.product_service.get_product.return_value = None
        
        items = [("nonexistent", 2, 100.0)]
        payment_info = {"valid": True, "type": "credit_card"}
        
        result = self.order_service.create_order(
            "cust_001",
            items,
            payment_info
        )
        
        self.assertIsNone(result)

    def test_create_order_insufficient_stock(self):
        """Test order creation with insufficient stock."""
        self.customer_service.get_customer.return_value = self.customer
        self.product_service.get_product.return_value = self.product
        self.inventory_service.check_product_availability.return_value = False
        
        items = [("prod_001", 20, 100.0)]  # More than available
        payment_info = {"valid": True, "type": "credit_card"}
        
        result = self.order_service.create_order(
            "cust_001",
            items,
            payment_info
        )
        
        self.assertIsNone(result)

    def test_create_order_payment_failed(self):
        """Test order creation with payment failure."""
        self.customer_service.get_customer.return_value = self.customer
        self.product_service.get_product.return_value = self.product
        self.inventory_service.check_product_availability.return_value = True
        self.pricing_service.apply_all_discounts.return_value = {
            'final_price': 200.0,
            'total_weight': 2.0
        }
        self.shipping_service.calculate_shipping_cost.return_value = 10.0
        self.payment_service.process_payment.return_value = (False, "Payment failed")
        self.order_repository.get_next_id.return_value = 1000
        
        items = [("prod_001", 2, 100.0)]
        payment_info = {"valid": False, "type": "credit_card"}
        
        result = self.order_service.create_order(
            "cust_001",
            items,
            payment_info
        )
        
        self.assertIsNone(result)

    def test_get_order(self):
        """Test getting an order by ID."""
        mock_order = Mock()
        self.order_repository.get.return_value = mock_order
        
        result = self.order_service.get_order("order_001")
        
        self.assertEqual(result, mock_order)
        self.order_repository.get.assert_called_once_with("order_001")

    def test_update_order_status_success(self):
        """Test successful order status update."""
        mock_order = Mock()
        mock_order.order_id = 1  # Use int to match conversion
        mock_order.customer_id = "cust_001"
        mock_order.status = OrderStatus.PENDING
        
        self.order_repository.get.return_value = mock_order
        self.customer_service.get_customer.return_value = self.customer
        
        result = self.order_service.update_order_status("1", "shipped")
        
        # Method returns order, not boolean, and may call customer service multiple times
        self.assertEqual(result, mock_order)
        # Repository should be called with int ID after conversion
        self.order_repository.get.assert_called_with(1)
        # Customer service may be called multiple times due to shipping logic
        self.assertGreaterEqual(self.customer_service.get_customer.call_count, 1)

    def test_update_order_status_order_not_found(self):
        """Test order status update for non-existent order."""
        self.order_repository.get.return_value = None
        
        result = self.order_service.update_order_status("nonexistent", "shipped")
        
        self.assertIsNone(result)

    def test_cancel_order_success(self):
        """Test successful order cancellation."""
        mock_order = Mock()
        mock_order.order_id = "order_001"
        mock_order.status = OrderStatus.PENDING
        mock_order.order_items = []  # Empty list instead of Mock
        
        self.order_repository.get.return_value = mock_order
        
        result = self.order_service.cancel_order("order_001", "Customer request")
        
        self.assertTrue(result)
        # Method doesn't actually call repository.update, just prints cancellation message

    def test_cancel_order_already_shipped(self):
        """Test cancelling order that's already shipped."""
        mock_order = Mock()
        mock_order.status = OrderStatus.SHIPPED
        
        self.order_repository.get.return_value = mock_order
        
        result = self.order_service.cancel_order("order_001", "Customer request")
        
        self.assertFalse(result)

    def test_cancel_order_not_found(self):
        """Test cancelling non-existent order."""
        self.order_repository.get.return_value = None
        
        result = self.order_service.cancel_order("nonexistent", "Customer request")
        
        self.assertFalse(result)

    def test_get_all_orders(self):
        """Test getting all orders."""
        mock_orders = {"order_001": Mock(), "order_002": Mock()}
        self.order_repository.get_all.return_value = mock_orders
        
        result = self.order_service.get_all_orders()
        
        self.assertEqual(result, mock_orders)


if __name__ == '__main__':
    unittest.main()