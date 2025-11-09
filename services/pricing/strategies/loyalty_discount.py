"""Loyalty Points Discount Strategy - Discounts using customer loyalty points."""

class LoyaltyDiscountStrategyImpl:
    """Calculate discount based on loyalty points."""

    def calculate_discount(self, loyalty_points: int, current_subtotal: float) -> float:
        """
        Calculate loyalty points discount amount.

        Args:
            loyalty_points: Customer's loyalty points
            current_subtotal: Current subtotal after all multiplicative discounts

        Returns:
            Discount amount
        """
        if loyalty_points < 100:
            return 0.0
        max_discount = current_subtotal * 0.1
        points_discount = loyalty_points * 0.01
        return min(max_discount, points_discount)

    def calculate_points_used(self, discount_amount: float) -> int:
        """
        Calculate how many points were used for a given discount amount.
        """
        return int(discount_amount * 100)
