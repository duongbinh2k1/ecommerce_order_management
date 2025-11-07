"""Loyalty Points Discount Strategy - Discounts using customer loyalty points."""

from services.pricing.strategies import DiscountStrategy


class LoyaltyPointsDiscountStrategy(DiscountStrategy):
    """Calculate discount based on loyalty points."""

    def calculate_discount(
        self,
        loyalty_points: int,
        subtotal: float
    ) -> tuple[float, int]:
        """
        Calculate loyalty points discount.

        Args:
            loyalty_points: Customer's loyalty points
            subtotal: Current subtotal

        Returns:
            Tuple of (discount_amount, points_used)
        """
        if loyalty_points < 100:
            return 0.0, 0

        max_discount = subtotal * 0.1
        points_discount = loyalty_points * 0.01
        discount = min(max_discount, points_discount)
        points_used = int(discount * 100)

        return discount, points_used
