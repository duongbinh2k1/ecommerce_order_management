"""Membership Discount Strategy - Discounts based on customer tier."""

from services.pricing.strategies import DiscountStrategy
from domain.enums.membership_tier import MembershipTier


class MembershipDiscountStrategy(DiscountStrategy):
    """Calculate discount based on membership tier."""

    def calculate_discount(self, tier: MembershipTier, subtotal: float) -> float:
        """
        Calculate membership discount rate.

        Args:
            tier: Customer membership tier
            subtotal: Order subtotal (unused, kept for interface compatibility)

        Returns:
            Discount rate (0.0 to 1.0)
        """
        if tier == MembershipTier.GOLD:
            return 0.15
        elif tier == MembershipTier.SILVER:
            return 0.07
        elif tier == MembershipTier.BRONZE:
            return 0.03
        
        return 0.0
