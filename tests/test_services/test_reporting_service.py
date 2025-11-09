"""Test cases for ReportingService."""
import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta
from services.reporting_service import ReportingService
from domain.enums.order_status import OrderStatus


class TestReportingService(unittest.TestCase):
    """Test cases for ReportingService class."""

    def setUp(self) -> None:
        """Set up test dependencies."""
        self.customer_service = Mock()
        self.order_service = Mock()
        self.product_service = Mock()
        
        self.reporting_service = ReportingService(
            customer_service=self.customer_service,
            order_service=self.order_service,
            product_service=self.product_service
        )

    def test_get_customer_lifetime_value_with_orders(self) -> None:
        """Test customer lifetime value calculation with orders."""
        # Create customer with order history
        customer = Mock()
        customer.order_history = ['order_001', 'order_002', 'order_003']
        self.customer_service.get_customer.return_value = customer
        
        # Create orders with proper Money value structure
        order1 = Mock()
        order1.total_price = Mock()
        order1.total_price.value = 100.0
        order1.status = OrderStatus.DELIVERED
        
        order2 = Mock()
        order2.total_price = Mock()
        order2.total_price.value = 200.0
        order2.status = OrderStatus.SHIPPED
        
        order3 = Mock()
        order3.total_price = Mock()
        order3.total_price.value = 50.0
        order3.status = OrderStatus.CANCELLED
        
        # Mock get_all_orders to return dictionary of orders
        self.order_service.get_all_orders.return_value = {
            'order_001': order1,
            'order_002': order2,
            'order_003': order3
        }
        
        # Test
        ltv = self.reporting_service.get_customer_lifetime_value(101)
        
        # Should only count non-cancelled orders
        self.assertEqual(ltv, 300.0)
        self.customer_service.get_customer.assert_called_once_with(101)

    def test_get_customer_lifetime_value_customer_not_found(self) -> None:
        """Test LTV calculation when customer not found."""
        self.customer_service.get_customer.return_value = None
        
        ltv = self.reporting_service.get_customer_lifetime_value(999)
        
        self.assertEqual(ltv, 0.0)
        self.customer_service.get_customer.assert_called_once_with(999)

    def test_get_customer_lifetime_value_no_orders(self) -> None:
        """Test LTV calculation for customer with no orders."""
        customer = Mock()
        customer.customer_id = 102
        customer.order_history = []
        self.customer_service.get_customer.return_value = customer
        
        ltv = self.reporting_service.get_customer_lifetime_value(102)
        
        self.assertEqual(ltv, 0.0)

    def test_generate_sales_report_basic(self) -> None:
        """Test basic sales report generation."""
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        
        # Mock orders with proper structure
        order1 = Mock()
        order1.created_at = datetime(2024, 1, 15)
        order1.status = OrderStatus.DELIVERED
        order1.total_price = Mock()
        order1.total_price.value = 100.0
        order1.items = []
        
        order2 = Mock()
        order2.created_at = datetime(2024, 1, 20)
        order2.status = OrderStatus.SHIPPED
        order2.total_price = Mock()
        order2.total_price.value = 200.0
        order2.items = []
        
        # Mock services
        self.order_service.get_all_orders.return_value = {
            'order1': order1,
            'order2': order2
        }
        self.product_service.get_all_products.return_value = {}
        self.customer_service.get_all_customers.return_value = {}
        
        report = self.reporting_service.generate_sales_report(start_date, end_date)
        
        self.assertEqual(report.total_sales, 300.0)
        self.assertEqual(report.total_orders, 2)
        self.assertEqual(report.cancelled_orders, 0)

    def test_generate_sales_report_with_cancelled_orders(self) -> None:
        """Test sales report with cancelled orders."""
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        
        # Mock orders including cancelled ones
        order1 = Mock()
        order1.created_at = datetime.now() - timedelta(days=3)
        order1.total_price = Mock()
        order1.total_price.value = 150.0
        order1.status = OrderStatus.CANCELLED
        order1.items = []
        
        order2 = Mock()
        order2.created_at = datetime.now() - timedelta(days=1)
        order2.total_price = Mock()
        order2.total_price.value = 300.0
        order2.status = OrderStatus.DELIVERED
        order2.items = []
        
        # Mock services
        self.order_service.get_all_orders.return_value = {
            "1": order1,
            "2": order2
        }
        self.product_service.get_all_products.return_value = {}
        self.customer_service.get_all_customers.return_value = {}
        
        report = self.reporting_service.generate_sales_report(start_date, end_date)
        
        self.assertEqual(report.total_sales, 300.0)  # Only non-cancelled
        self.assertEqual(report.total_orders, 1)
        self.assertEqual(report.cancelled_orders, 1)

    def test_generate_sales_report_empty_date_range(self) -> None:
        """Test sales report with no orders in date range."""
        start_date = datetime.now() + timedelta(days=1)  # Future date
        end_date = datetime.now() + timedelta(days=7)
        
        order1 = Mock()
        order1.created_at = datetime.now() - timedelta(days=3)
        order1.total_price = Mock()
        order1.total_price.value = 100.0
        order1.status = OrderStatus.DELIVERED
        
        # Mock customer service for top_customers calculation
        self.customer_service.get_all_customers.return_value = {}
        self.product_service.get_all_products.return_value = {}
        
        self.order_service.get_all_orders.return_value = {"1": order1}
        
        report = self.reporting_service.generate_sales_report(start_date, end_date)
        
        self.assertEqual(report.total_sales, 0)
        self.assertEqual(report.total_orders, 0)
        self.assertEqual(report.cancelled_orders, 0)


if __name__ == '__main__':
    unittest.main()