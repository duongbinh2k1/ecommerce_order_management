"""Reporting Service - Handles sales reports and analytics."""

from typing import TYPE_CHECKING
import datetime
from domain.enums.order_status import OrderStatus

if TYPE_CHECKING:
    from services.customer_service import CustomerService
    from services.order_service import OrderService
    from services.product_service import ProductService


class ReportingService:
    """Service for generating reports and analytics."""

    def __init__(
        self,
        customer_service: 'CustomerService',
        order_service: 'OrderService',
        product_service: 'ProductService'
    ) -> None:
        """Initialize reporting service with dependencies."""
        self.__customer_service = customer_service
        self.__order_service = order_service
        self.__product_service = product_service

    def get_customer_lifetime_value(self, customer_id: int) -> float:
        """
        Calculate customer lifetime value.

        Args:
            customer_id: Customer identifier

        Returns:
            Total value of all non-cancelled orders
        """
        customer = self.__customer_service.get_customer(customer_id)
        if not customer:
            return 0.0

        total_value = 0.0
        orders = self.__order_service.get_all_orders()

        for order_id in customer.order_history:
            order = orders.get(str(order_id))
            if order and order.status != OrderStatus.CANCELLED:
                total_value += order.total_price.value

        return total_value

    def generate_sales_report(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime
    ) -> dict:
        """
        Generate comprehensive sales report for date range.

        Args:
            start_date: Report start date
            end_date: Report end date

        Returns:
            Report dictionary with sales metrics
        """
        report = {
            'total_sales': 0.0,
            'total_orders': 0,
            'cancelled_orders': 0,
            'products_sold': {},
            'revenue_by_category': {},
            'top_customers': []
        }

        orders = self.__order_service.get_all_orders()
        products = self.__product_service.get_all_products()

        # Process all orders in date range
        for order in orders.values():
            if start_date <= order.created_at <= end_date:
                if order.status != OrderStatus.CANCELLED:
                    report['total_sales'] += order.total_price.value
                    report['total_orders'] += 1

                    # Aggregate products sold
                    for item in order.items:
                        product = products.get(item.product_id)
                        if product:
                            # Count products sold
                            if product.product_id not in report['products_sold']:
                                report['products_sold'][product.product_id] = 0
                            report['products_sold'][product.product_id] += item.quantity

                            # Revenue by category
                            if product.category not in report['revenue_by_category']:
                                report['revenue_by_category'][product.category] = 0.0

                            # Extract Money value
                            item_price = item.unit_price.value
                            report['revenue_by_category'][product.category] += (
                                item.quantity * item_price
                            )
                else:
                    report['cancelled_orders'] += 1

        # Calculate top customers
        report['top_customers'] = self.__get_top_customers(limit=10)

        return report

    def __get_top_customers(self, limit: int = 10) -> list[tuple[str, float]]:
        """
        Get top customers by lifetime value.

        Args:
            limit: Number of top customers to return

        Returns:
            List of (customer_id, lifetime_value) tuples
        """
        customer_spending = {}
        customers = self.__customer_service.get_all_customers()

        for customer_id in customers.keys():
            customer_spending[customer_id] = self.get_customer_lifetime_value(
                customer_id)

        sorted_customers = sorted(
            customer_spending.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_customers[:limit]

    def get_product_performance(self) -> dict[str, int]:
        """
        Get product sales performance.

        Returns:
            Dictionary of product_id -> total_quantity_sold
        """
        products_sold = {}
        orders = self.__order_service.get_all_orders()

        for order in orders.values():
            if order.status != OrderStatus.CANCELLED:
                for item in order.items:
                    if item.product_id not in products_sold:
                        products_sold[item.product_id] = 0
                    products_sold[item.product_id] += item.quantity

        return products_sold

    def get_category_revenue(self) -> dict[str, float]:
        """
        Get revenue breakdown by product category.

        Returns:
            Dictionary of category -> total_revenue
        """
        revenue_by_category = {}
        orders = self.__order_service.get_all_orders()
        products = self.__product_service.get_all_products()

        for order in orders.values():
            if order.status != OrderStatus.CANCELLED:
                for item in order.items:
                    product = products.get(item.product_id)
                    if product:
                        if product.category not in revenue_by_category:
                            revenue_by_category[product.category] = 0.0

                        item_price = item.unit_price.value
                        revenue_by_category[product.category] += (
                            item.quantity * item_price
                        )

        return revenue_by_category
