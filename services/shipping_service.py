"""Shipping Service - Handles shipping calculations and logistics."""

from domain.enums.shipping_method import ShippingMethod
from domain.enums.membership_tier import MembershipTier


class ShippingService:
    """Service for shipping cost calculations and delivery estimates."""

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
