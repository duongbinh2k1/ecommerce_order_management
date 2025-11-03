"""Shipping Service - Handles shipping calculations and logistics."""

from typing import TYPE_CHECKING
from domain.enums.shipping_method import ShippingMethod
from domain.enums.membership_tier import MembershipTier

if TYPE_CHECKING:
    from domain.models.customer import Customer


class ShippingService:
    """Service for shipping cost calculations and shipment management."""

    def __init__(self) -> None:
        """Initialize the shipping service."""
        self.__tracking_numbers: dict[str, dict] = {}

    def calculate_shipping_cost(
        self,
        shipping_method: ShippingMethod,
        total_weight: float,
        subtotal: float,
        customer_tier: MembershipTier
    ) -> float:
        """
        Calculate shipping cost based on method, weight, and customer tier.

        Args:
            shipping_method: Selected shipping method
            total_weight: Total package weight in kg
            subtotal: Order subtotal (for free shipping threshold)
            customer_tier: Customer's membership tier

        Returns:
            Shipping cost
        """
        shipping_cost = 0.0

        if shipping_method == ShippingMethod.EXPRESS:
            shipping_cost = 25 + (total_weight * 0.5)
            # Gold members get 50% off express shipping
            if customer_tier == MembershipTier.GOLD:
                shipping_cost *= 0.5

        elif shipping_method == ShippingMethod.STANDARD:
            if subtotal < 50:
                shipping_cost = 5 + (total_weight * 0.2)
            else:
                shipping_cost = 0  # Free shipping over $50

        elif shipping_method == ShippingMethod.OVERNIGHT:
            shipping_cost = 50 + (total_weight * 1.0)

        return shipping_cost

    def create_shipment(
        self,
        order_id: str,
        shipping_method: ShippingMethod,
        address: str
    ) -> str:
        """
        Create a new shipment and generate tracking number.

        Args:
            order_id: Order identifier
            shipping_method: Shipping method
            address: Delivery address

        Returns:
            Tracking number
        """
        import random
        tracking_number = f"TRACK-{order_id}-{random.randint(1000, 9999)}"

        self.__tracking_numbers[tracking_number] = {
            'order_id': order_id,
            'shipping_method': shipping_method.value,
            'address': address,
            'status': 'pending'
        }

        return tracking_number

    def update_shipment_status(
        self,
        tracking_number: str,
        new_status: str
    ) -> bool:
        """
        Update shipment status.

        Args:
            tracking_number: Tracking number
            new_status: New status (e.g., 'in_transit', 'delivered')

        Returns:
            True if successful, False if tracking number not found
        """
        if tracking_number in self.__tracking_numbers:
            self.__tracking_numbers[tracking_number]['status'] = new_status
            return True
        return False

    def get_tracking_info(self, tracking_number: str) -> dict:
        """
        Get shipment tracking information.

        Args:
            tracking_number: Tracking number

        Returns:
            Tracking information dictionary or empty dict if not found
        """
        return self.__tracking_numbers.get(tracking_number, {})
