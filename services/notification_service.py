"""Notification Service - Handles customer notifications."""

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models.customer import Customer
    from domain.models.order import Order


class NotificationService:
    """Service for sending notifications to customers."""

    def __init__(self) -> None:
        """Initialize the notification service."""
        self.__notification_log: list[dict[str, Any]] = []

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

        self.__notification_log.append({
            'customer_id': customer.customer_id,
            'order_id': order.order_id,
            'type': 'order_confirmation',
            'total': order.total_price.value
        })

    def send_shipment_notification(
        self,
        customer: 'Customer',
        order_id: int,
        tracking_number: str
    ) -> None:
        """
        Send shipment notification with tracking.

        Args:
            customer: Customer receiving the shipment
            order_id: Order identifier
            tracking_number: Tracking number
        """
        # Format exactly like legacy system
        print(f"To: {customer.email.value}: Order {order_id} status changed to shipped")

        self.__notification_log.append({
            'customer_id': customer.customer_id,
            'order_id': order_id,
            'type': 'shipment',
            'tracking_number': tracking_number
        })

    def send_low_stock_alert(
        self,
        supplier_email: str,
        product_name: str,
        current_stock: int
    ) -> None:
        """
        Send low stock alert to supplier.

        Args:
            supplier_email: Supplier email address
            product_name: Product name
            current_stock: Current stock level
        """
        message = (
            f"Low Stock Alert!\n"
            f"Product: {product_name}\n"
            f"Current stock: {current_stock}"
        )

        print(f"[EMAIL to {supplier_email}] {message}")

        self.__notification_log.append({
            'supplier_email': supplier_email,
            'type': 'low_stock_alert',
            'message': message
        })

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
        message = (
            f"Congratulations {customer.name}!\n"
            f"Your membership has been upgraded to {new_tier}!"
        )

        print(f"[EMAIL to {customer.email.value}] {message}")

        self.__notification_log.append({
            'customer_id': customer.customer_id,
            'type': 'membership_upgrade',
            'message': message
        })

    def get_notification_log(self) -> list[dict[str, Any]]:
        """
        Get all notification logs.

        Returns:
            List of notification records
        """
        return self.__notification_log.copy()
