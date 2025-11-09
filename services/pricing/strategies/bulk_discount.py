"""Bulk Discount Strategy - Discounts for large quantity purchases."""

from services.pricing.strategies import DiscountStrategy


class BulkDiscountStrategy(DiscountStrategy):
    """Calculate discount based on bulk purchase."""

    def calculate_discount(self, total_items: int, subtotal: float) -> float:
        """
        Calculate bulk discount rate.

        Args:
            total_items: Total number of items in order
            subtotal: Current subtotal (unused, kept for interface compatibility)

        Returns:
            Discount rate (0.0 to 1.0)
        """
        if total_items >= 10:
            return 0.05
        elif total_items >= 5:
            return 0.02
        
        return 0.0
