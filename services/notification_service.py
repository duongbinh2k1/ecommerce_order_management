"""Notification Service - Handles customer notifications."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models.customer import Customer
    from domain.models.order import Order


class NotificationService:
    """Service for sending notifications to customers (print-based like legacy)."""

    def send_order_confirmation(
        self,
        customer: 'Customer',
        order: 'Order'
    ) -> None:
        """
        Send order confirmation notification.

        Args:
            customer: Customer who placed the order
            order: Order details
        """
        # Format exactly like legacy system
        print(f"To: {customer.email.value}: Order {order.order_id} confirmed! Total: ${order.total_price.value:.2f}")
        if hasattr(customer, 'phone') and customer.phone:
            print(f"SMS to {customer.phone.value}: Order {order.order_id} confirmed")

    def send_shipment_notification(
        self,
        customer: 'Customer',
        order_id: int
    ) -> None:
        """
        Send shipment notification.

        Args:
            customer: Customer receiving the shipment
            order_id: Order identifier
        """
        # Format exactly like legacy system
        print(f"To: {customer.email.value}: Order {order_id} status changed to shipped")

    def send_low_stock_alert(
        self,
        supplier_email: str,
        product_name: str
    ) -> None:
        """
        Send low stock alert to supplier.

        Args:
            supplier_email: Supplier email address
            product_name: Product name
        """
        # Format exactly like legacy system
        print(f"Email to {supplier_email}: Low stock alert for {product_name}")

    def send_membership_upgrade(
        self,
        customer: 'Customer',
        new_tier: str
    ) -> None:
        """
        Send membership upgrade notification.

        Args:
            customer: Customer who was upgraded
            new_tier: New membership tier
        """
        # Format exactly like legacy system
        message = f"Customer {customer.name} upgraded to {new_tier}!"
        print(message)

    def send_marketing_email(
        self,
        customer_email: str,
        message: str
    ) -> None:
        """
        Send marketing email to customer.

        Args:
            customer_email: Customer email address
            message: Marketing message
        """
        # Format exactly like legacy system
        print(f"Email to {customer_email}: {message}")

    def send_order_cancellation(
        self,
        customer: 'Customer',
        order_id: int,
        reason: str
    ) -> None:
        """
        Send order cancellation notification.

        Args:
            customer: Customer who cancelled order
            order_id: Order identifier
            reason: Cancellation reason
        """
        # Format exactly like legacy system
        print(f"To: {customer.email.value}: Order {order_id} has been cancelled. Reason: {reason}")
