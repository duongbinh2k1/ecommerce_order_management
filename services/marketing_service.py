"""Marketing Service - Handles customer segmentation and campaigns."""

from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from services.customer_service import CustomerService
    from services.order_service import OrderService


class MarketingService:
    """Service for marketing campaigns and customer communications."""

    def __init__(
        self,
        customer_service: 'CustomerService',
        order_service: 'OrderService'
    ) -> None:
        """Initialize marketing service with dependencies."""
        self.__customer_service = customer_service
        self.__order_service = order_service

    def send_marketing_email(
        self,
        customer_segment: str,
        message: str
    ) -> int:
        """
        Send marketing email to a customer segment.

        Args:
            customer_segment: Segment type ('all', 'gold', 'inactive', etc.)
            message: Email message content

        Returns:
            Number of emails sent
        """
        count = 0
        customers = self.__customer_service.get_all_customers()

        for customer in customers.values():
            send = False

            if customer_segment == 'all':
                send = True
            elif customer_segment == 'gold':
                send = customer.membership_tier.value == 'gold'
            elif customer_segment == 'silver':
                send = customer.membership_tier.value == 'silver'
            elif customer_segment == 'bronze':
                send = customer.membership_tier.value == 'bronze'
            elif customer_segment == 'inactive':
                # Check if customer has ordered in last 90 days
                send = self.__is_customer_inactive(customer.customer_id)

            if send:
                print(f"[MARKETING EMAIL to {customer.email.value}] {message}")
                count += 1

        return count

    def __is_customer_inactive(
        self,
        customer_id: str,
        days_threshold: int = 90
    ) -> bool:
        """
        Check if customer is inactive (no orders in threshold days).

        Args:
            customer_id: Customer identifier
            days_threshold: Number of days to check

        Returns:
            True if customer is inactive
        """
        customer = self.__customer_service.get_customer(customer_id)
        if not customer:
            return False

        cutoff = datetime.datetime.now() - datetime.timedelta(days=days_threshold)
        orders = self.__order_service.get_all_orders()

        for order_id in customer.order_history:
            order = orders.get(str(order_id))
            if order and order.created_at > cutoff:
                return False  # Has recent order

        return True  # No recent orders

    def get_inactive_customers(self, days_threshold: int = 90) -> list:
        """
        Get list of inactive customers.

        Args:
            days_threshold: Number of days to consider inactive

        Returns:
            List of inactive customer IDs
        """
        inactive = []
        customers = self.__customer_service.get_all_customers()

        for customer_id in customers.keys():
            if self.__is_customer_inactive(customer_id, days_threshold):
                inactive.append(customer_id)

        return inactive

    def segment_customers_by_value(self) -> dict:
        """
        Segment customers by lifetime value.

        Returns:
            Dictionary with customer segments
        """
        
        # Would need ReportingService injected, for now return placeholder
        return {
            'high_value': [],  # LTV > 1000
            'medium_value': [],  # LTV 500-1000
            'low_value': []  # LTV < 500
        }
