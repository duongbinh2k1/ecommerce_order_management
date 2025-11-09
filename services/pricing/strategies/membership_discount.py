"""Membership Discount Strategy - Discounts based on customer tier."""
from domain.enums.membership_tier import MembershipTier

class MembershipDiscountStrategyImpl:
    """Calculate discount based on membership tier."""

    def calculate_discount(self, tier: MembershipTier, subtotal: float) -> float:
        """
        Calculate membership discount amount.

        Args:
            tier: Customer membership tier
            subtotal: Order subtotal

        Returns:
            Discount amount to subtract from subtotal
        """
        if tier == MembershipTier.GOLD:
            rate = 0.15
        elif tier == MembershipTier.SILVER:
            rate = 0.07
        elif tier == MembershipTier.BRONZE:
            rate = 0.03
        else:
            rate = 0.0
        return subtotal - (subtotal * (1 - rate))
