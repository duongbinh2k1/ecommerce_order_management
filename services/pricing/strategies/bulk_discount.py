"""Bulk Discount Strategy - Discounts for large quantity purchases."""

from services.pricing.strategies import DiscountStrategy


class BulkDiscountStrategy(DiscountStrategy):
    """Calculate discount based on bulk purchase."""

    def calculate_discount(self, total_items: int, subtotal: float) -> float:
        """
        Calculate bulk discount.

        Args:
            total_items: Total number of items in order
            subtotal: Current subtotal

        Returns:
            Discount amount
        """
        discount_rate = 0.0
        if total_items >= 10:
            discount_rate = 0.05
        elif total_items >= 5:
            discount_rate = 0.02

        return subtotal * discount_rate
