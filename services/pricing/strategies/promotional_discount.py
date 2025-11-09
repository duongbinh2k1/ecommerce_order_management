"""Promotional Discount Strategy - Discounts based on promo codes."""
from typing import Optional, TYPE_CHECKING
import datetime
from domain.enums.product_category import ProductCategory

if TYPE_CHECKING:
    from domain.models.promotion import Promotion
    from domain.models.order_item import OrderItem
    from domain.models.product import Product

class PromotionalDiscountStrategyImpl:
    """Calculate discount based on promotional code."""

    def calculate_discount(
        self,
        promotion: Optional['Promotion'],
        original_subtotal: float,
        current_subtotal: float,
        order_items: list['OrderItem'], 
        products: dict[int, 'Product']
    ) -> float:
        """
        Calculate promotional discount amount.
        Legacy logic: Check eligibility against original_subtotal but apply multiplicatively to current_subtotal.

        Args:
            promotion: Promotion object (or None)
            original_subtotal: Original subtotal for min purchase validation
            current_subtotal: Current subtotal (after membership discount) to apply promo to
            order_items: List of order items
            products: Dictionary of products

        Returns:
            Discount amount to subtract from current_subtotal
        """
        if not promotion:
            return 0.0
        if datetime.datetime.now() > promotion.valid_until:
            return 0.0
        if original_subtotal < promotion.min_purchase.value:
            return 0.0
        applicable = False
        for item in order_items:
            product = products.get(item.product_id)
            if product:
                if promotion.category == ProductCategory.ALL or product.category == promotion.category:
                    applicable = True
                    break
        if applicable:
            rate = promotion.discount_percent / 100
            return current_subtotal - (current_subtotal * (1 - rate))
        return 0.0
