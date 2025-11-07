"""
Test MarketingService - customer segmentation and campaign functionality
Tests marketing email sending and customer segmentation
"""
import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta
from services.marketing_service import MarketingService


class TestMarketingService(unittest.TestCase):
    """Test MarketingService marketing functionality."""

    def setUp(self):
        """Set up test dependencies."""
        self.customer_service = Mock()
        self.order_service = Mock()
        self.marketing_service = MarketingService(
            self.customer_service,
            self.order_service
        )

        # Create mock customers
        self.gold_customer = Mock()
        self.gold_customer.customer_id = "cust_001"
        self.gold_customer.email = Mock()
        self.gold_customer.email.value = "gold@example.com"
        self.gold_customer.membership_tier = Mock()
        self.gold_customer.membership_tier.value = "gold"
        self.gold_customer.order_history = ["order_001"]

        self.silver_customer = Mock()
        self.silver_customer.customer_id = "cust_002"
        self.silver_customer.email = Mock()
        self.silver_customer.email.value = "silver@example.com"
        self.silver_customer.membership_tier = Mock()
        self.silver_customer.membership_tier.value = "silver"
        self.silver_customer.order_history = ["order_002"]

        self.bronze_customer = Mock()
        self.bronze_customer.customer_id = "cust_003"
        self.bronze_customer.email = Mock()
        self.bronze_customer.email.value = "bronze@example.com"
        self.bronze_customer.membership_tier = Mock()
        self.bronze_customer.membership_tier.value = "bronze"
        self.bronze_customer.order_history = []

    def test_send_marketing_email_to_all(self):
        """Test sending marketing email to all customers."""
        self.customer_service.get_all_customers.return_value = {
            "cust_001": self.gold_customer,
            "cust_002": self.silver_customer,
            "cust_003": self.bronze_customer
        }

        count = self.marketing_service.send_marketing_email(
            "all", "Welcome to our sale!"
        )

        self.assertEqual(count, 3)

    def test_send_marketing_email_to_gold(self):
        """Test sending marketing email to gold customers only."""
        self.customer_service.get_all_customers.return_value = {
            "cust_001": self.gold_customer,
            "cust_002": self.silver_customer,
            "cust_003": self.bronze_customer
        }

        count = self.marketing_service.send_marketing_email(
            "gold", "Exclusive gold member offer!"
        )

        self.assertEqual(count, 1)

    def test_send_marketing_email_to_silver(self):
        """Test sending marketing email to silver customers only."""
        self.customer_service.get_all_customers.return_value = {
            "cust_001": self.gold_customer,
            "cust_002": self.silver_customer,
            "cust_003": self.bronze_customer
        }

        count = self.marketing_service.send_marketing_email(
            "silver", "Silver member special!"
        )

        self.assertEqual(count, 1)

    def test_send_marketing_email_to_bronze(self):
        """Test sending marketing email to bronze customers only."""
        self.customer_service.get_all_customers.return_value = {
            "cust_001": self.gold_customer,
            "cust_002": self.silver_customer,
            "cust_003": self.bronze_customer
        }

        count = self.marketing_service.send_marketing_email(
            "bronze", "Bronze member discount!"
        )

        self.assertEqual(count, 1)

    def test_send_marketing_email_to_inactive(self):
        """Test sending marketing email to inactive customers."""
        # Mock customers
        self.customer_service.get_all_customers.return_value = {
            "cust_001": self.gold_customer,
            "cust_003": self.bronze_customer
        }

        # Mock that gold customer has recent order, bronze doesn't
        def get_customer(customer_id):
            return {
                "cust_001": self.gold_customer,
                "cust_003": self.bronze_customer
            }.get(customer_id)
        
        self.customer_service.get_customer.side_effect = get_customer

        # Mock recent order for gold customer
        recent_order = Mock()
        recent_order.created_at = datetime.now() - timedelta(days=30)

        # Mock old order for bronze customer
        old_order = Mock()
        old_order.created_at = datetime.now() - timedelta(days=120)

        self.order_service.get_all_orders.return_value = {
            "order_001": recent_order,
            "order_002": old_order
        }

        count = self.marketing_service.send_marketing_email(
            "inactive", "We miss you!"
        )

        # Bronze customer should be considered inactive
        self.assertEqual(count, 1)

    def test_get_inactive_customers(self):
        """Test getting list of inactive customers."""
        self.customer_service.get_all_customers.return_value = {
            "cust_001": self.gold_customer,
            "cust_003": self.bronze_customer
        }

        # Mock customer retrieval
        def get_customer(customer_id):
            return {
                "cust_001": self.gold_customer,
                "cust_003": self.bronze_customer
            }.get(customer_id)
        
        self.customer_service.get_customer.side_effect = get_customer

        # Mock orders
        recent_order = Mock()
        recent_order.created_at = datetime.now() - timedelta(days=30)

        old_order = Mock()
        old_order.created_at = datetime.now() - timedelta(days=120)

        self.order_service.get_all_orders.return_value = {
            "order_001": recent_order,
            "order_002": old_order
        }

        inactive = self.marketing_service.get_inactive_customers(90)

        # Bronze customer should be inactive (no recent orders)
        self.assertEqual(len(inactive), 1)
        self.assertIn("cust_003", inactive)

    def test_get_inactive_customers_custom_threshold(self):
        """Test getting inactive customers with custom threshold."""
        self.customer_service.get_all_customers.return_value = {
            "cust_001": self.gold_customer
        }

        self.customer_service.get_customer.return_value = self.gold_customer

        # Mock order that's 45 days old
        order = Mock()
        order.created_at = datetime.now() - timedelta(days=45)

        self.order_service.get_all_orders.return_value = {
            "order_001": order
        }

        # With 30-day threshold, should be inactive
        inactive_30 = self.marketing_service.get_inactive_customers(30)
        self.assertEqual(len(inactive_30), 1)

        # With 60-day threshold, should not be inactive
        inactive_60 = self.marketing_service.get_inactive_customers(60)
        self.assertEqual(len(inactive_60), 0)

    def test_segment_customers_by_value(self):
        """Test customer segmentation by value."""
        segments = self.marketing_service.segment_customers_by_value()

        # Should return placeholder structure
        self.assertIn('high_value', segments)
        self.assertIn('medium_value', segments)
        self.assertIn('low_value', segments)
        self.assertIsInstance(segments['high_value'], list)
        self.assertIsInstance(segments['medium_value'], list)
        self.assertIsInstance(segments['low_value'], list)

    def test_send_marketing_email_no_customers(self):
        """Test sending marketing email when no customers exist."""
        self.customer_service.get_all_customers.return_value = {}

        count = self.marketing_service.send_marketing_email(
            "all", "Sale announcement!"
        )

        self.assertEqual(count, 0)


if __name__ == '__main__':
    unittest.main()