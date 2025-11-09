"""
Test NotificationService - Print-based notifications like legacy system
Tests notification sending without logging (matching legacy behavior)
"""
import unittest
from unittest.mock import Mock
from services.notification_service import NotificationService
from domain.value_objects.email import Email
from domain.value_objects.phone_number import PhoneNumber
from domain.value_objects.money import Money


class TestNotificationService(unittest.TestCase):
    """Test NotificationService without logging functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.notification_service = NotificationService()
        
        # Mock customer
        self.customer = Mock()
        self.customer.customer_id = 101
        self.customer.name = "John Doe" 
        self.customer.email = Email("john@example.com")
        self.customer.phone = PhoneNumber("555-0123")
        
        # Mock order
        self.order = Mock()
        self.order.order_id = 1
        self.order.total_price = Money(150.50)

    def test_send_order_confirmation(self) -> None:
        """Test sending order confirmation notification."""
        # Should only print, no exceptions
        self.notification_service.send_order_confirmation(
            self.customer, self.order
        )
        # Test passes if no exception is raised

    def test_send_order_confirmation_without_phone(self) -> None:
        """Test order confirmation when customer has no phone."""
        customer_no_phone = Mock()
        customer_no_phone.customer_id = 102
        customer_no_phone.name = "Jane Doe"
        customer_no_phone.email = Email("jane@example.com")
        # No phone attribute
        
        self.notification_service.send_order_confirmation(
            customer_no_phone, self.order
        )
        # Test passes if no exception is raised

    def test_send_shipment_notification(self) -> None:
        """Test sending shipment notification."""
        self.notification_service.send_shipment_notification(
            self.customer, 2
        )
        # Test passes if no exception is raised

    def test_send_low_stock_alert(self) -> None:
        """Test sending low stock alert to supplier."""
        self.notification_service.send_low_stock_alert(
            "supplier@company.com", "Widget Pro"
        )
        # Test passes if no exception is raised

    def test_send_membership_upgrade(self) -> None:
        """Test sending membership upgrade notification."""
        self.notification_service.send_membership_upgrade(
            self.customer, "Gold"
        )
        # Test passes if no exception is raised

    def test_send_marketing_email(self) -> None:
        """Test sending marketing email."""
        self.notification_service.send_marketing_email(
            "customer@example.com", "Special discount just for you!"
        )
        # Test passes if no exception is raised

    def test_send_order_cancellation(self) -> None:
        """Test sending order cancellation notification."""
        self.notification_service.send_order_cancellation(
            self.customer, 3, "Customer request"
        )
        # Test passes if no exception is raised


if __name__ == '__main__':
    unittest.main()