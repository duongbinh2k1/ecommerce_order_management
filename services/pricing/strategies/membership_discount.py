"""Membership Discount Strategy - Discounts based on customer tier."""

from services.pricing.strategies import DiscountStrategy
from domain.enums.membership_tier import MembershipTier


class MembershipDiscountStrategy(DiscountStrategy):
    """Calculate discount based on membership tier."""

    def calculate_discount(self, tier: MembershipTier, subtotal: float) -> float:
        """
        Calculate membership discount.

        Args:
            tier: Customer membership tier
            subtotal: Order subtotal

        Returns:
            Discount amount
        """
        discount_rate = 0.0
        if tier == MembershipTier.GOLD:
            discount_rate = 0.15
        elif tier == MembershipTier.SILVER:
            discount_rate = 0.07
        elif tier == MembershipTier.BRONZE:
            discount_rate = 0.03

        return subtotal * discount_rate
