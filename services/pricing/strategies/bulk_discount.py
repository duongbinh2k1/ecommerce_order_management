"""Bulk Discount Strategy - Discounts for large quantity purchases."""

class BulkDiscountStrategyImpl:
    """Calculate discount based on bulk purchase."""

    def calculate_discount(self, total_items: int, current_subtotal: float) -> float:
        """
        Calculate bulk discount amount.
        Legacy logic: Apply multiplicatively to current subtotal.

        Args:
            total_items: Total number of items in order
            current_subtotal: Current subtotal to apply discount to

        Returns:
            Discount amount to subtract from current_subtotal
        """
        if total_items >= 10:
            rate = 0.05
        elif total_items >= 5:
            rate = 0.02
        else:
            rate = 0.0
        return current_subtotal - (current_subtotal * (1 - rate))
