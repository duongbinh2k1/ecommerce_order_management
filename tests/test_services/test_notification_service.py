"""
Test NotificationService - customer notification functionality
Tests order confirmations, shipment notifications, and alerts
"""
import unittest
from unittest.mock import Mock
from services.notification_service import NotificationService


class TestNotificationService(unittest.TestCase):
    """Test NotificationService notification functionality."""

    def setUp(self):
        """Set up test dependencies."""
        self.notification_service = NotificationService()

        # Create mock customer
        self.customer = Mock()
        self.customer.customer_id = "cust_001"
        self.customer.name = "John Doe"
        self.customer.email = Mock()
        self.customer.email.value = "john@example.com"

        # Create mock order
        self.order = Mock()
        self.order.order_id = "order_001"
        self.order.total_price = Mock()
        self.order.total_price.value = 150.50
        self.order.status = Mock()
        self.order.status.value = "confirmed"

    def test_send_order_confirmation(self):
        """Test sending order confirmation notification."""
        self.notification_service.send_order_confirmation(
            self.customer, self.order
        )

        log = self.notification_service.get_notification_log()
        self.assertEqual(len(log), 1)

        notification = log[0]
        self.assertEqual(notification['customer_id'], "cust_001")
        self.assertEqual(notification['order_id'], "order_001")
        self.assertEqual(notification['type'], "order_confirmation")
        self.assertIn("Order Confirmation for John Doe", notification['message'])
        self.assertIn("Order ID: order_001", notification['message'])
        self.assertIn("Total: $150.50", notification['message'])
        self.assertIn("Status: confirmed", notification['message'])

    def test_send_shipment_notification(self):
        """Test sending shipment notification."""
        self.notification_service.send_shipment_notification(
            self.customer, "order_002", "TRACK123456"
        )

        log = self.notification_service.get_notification_log()
        self.assertEqual(len(log), 1)

        notification = log[0]
        self.assertEqual(notification['customer_id'], "cust_001")
        self.assertEqual(notification['order_id'], "order_002")
        self.assertEqual(notification['type'], "shipment")
        self.assertIn("Your order order_002 has been shipped!", notification['message'])
        self.assertIn("Tracking number: TRACK123456", notification['message'])

    def test_send_low_stock_alert(self):
        """Test sending low stock alert to supplier."""
        self.notification_service.send_low_stock_alert(
            "supplier@company.com", "Widget Pro", 5
        )

        log = self.notification_service.get_notification_log()
        self.assertEqual(len(log), 1)

        notification = log[0]
        self.assertEqual(notification['supplier_email'], "supplier@company.com")
        self.assertEqual(notification['type'], "low_stock_alert")
        self.assertIn("Low Stock Alert!", notification['message'])
        self.assertIn("Product: Widget Pro", notification['message'])
        self.assertIn("Current stock: 5", notification['message'])

    def test_send_membership_upgrade(self):
        """Test sending membership upgrade notification."""
        self.notification_service.send_membership_upgrade(
            self.customer, "Gold"
        )

        log = self.notification_service.get_notification_log()
        self.assertEqual(len(log), 1)

        notification = log[0]
        self.assertEqual(notification['customer_id'], "cust_001")
        self.assertEqual(notification['type'], "membership_upgrade")
        self.assertIn("Congratulations John Doe!", notification['message'])
        self.assertIn("Your membership has been upgraded to Gold!", notification['message'])

    def test_multiple_notifications(self):
        """Test sending multiple notifications and checking log."""
        # Send order confirmation
        self.notification_service.send_order_confirmation(
            self.customer, self.order
        )

        # Send shipment notification
        self.notification_service.send_shipment_notification(
            self.customer, "order_001", "SHIP789"
        )

        # Send membership upgrade
        self.notification_service.send_membership_upgrade(
            self.customer, "Silver"
        )

        log = self.notification_service.get_notification_log()
        self.assertEqual(len(log), 3)

        # Check types are different
        types = [notification['type'] for notification in log]
        self.assertIn("order_confirmation", types)
        self.assertIn("shipment", types)
        self.assertIn("membership_upgrade", types)

    def test_get_notification_log_returns_copy(self):
        """Test that get_notification_log returns a copy."""
        self.notification_service.send_order_confirmation(
            self.customer, self.order
        )

        log1 = self.notification_service.get_notification_log()
        log2 = self.notification_service.get_notification_log()

        # Should be equal but not the same object
        self.assertEqual(log1, log2)
        self.assertIsNot(log1, log2)

        # Modifying returned log shouldn't affect internal state
        log1.append({"test": "data"})
        log3 = self.notification_service.get_notification_log()
        self.assertNotEqual(len(log1), len(log3))

    def test_empty_notification_log(self):
        """Test getting notification log when no notifications sent."""
        log = self.notification_service.get_notification_log()
        
        self.assertEqual(len(log), 0)
        self.assertIsInstance(log, list)


if __name__ == '__main__':
    unittest.main()