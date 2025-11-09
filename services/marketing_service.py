"""Marketing Service - Handles customer segmentation and campaigns."""

from typing import TYPE_CHECKING
import datetime
from domain.enums.membership_tier import MembershipTier
from domain.enums.customer_segment import CustomerSegment

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
        customer_segment: CustomerSegment,
        message: str
    ) -> int:
        """
        Send marketing email to a customer segment.

        Args:
            customer_segment: Customer segment enum
            message: Email message content

        Returns:
            Number of emails sent
        """
        count = 0
        customers = self.__customer_service.get_all_customers()

        for customer in customers.values():
            send = False

            if customer_segment == CustomerSegment.ALL:
                send = True
            elif customer_segment == CustomerSegment.GOLD and customer.membership_tier == MembershipTier.GOLD:
                send = True
            elif customer_segment == CustomerSegment.INACTIVE:
                # Check if customer has ordered in last 90 days
                if self.__is_customer_inactive(customer.customer_id):
                    send = True

            if send:
                print(f"Email to {customer.email.value}: {message}")
                count += 1

        return count

    def __is_customer_inactive(
        self,
        customer_id: int,
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
            order = orders.get(order_id)
            if order and order.created_at > cutoff:
                return False

        return True
