"""Promotional Discount Strategy - Discounts based on promo codes."""

from typing import Optional, TYPE_CHECKING
import datetime
from services.pricing.strategies import DiscountStrategy

if TYPE_CHECKING:
    from domain.models.promotion import Promotion
    from domain.models.order_item import OrderItem
    from domain.models.product import Product


class PromotionalDiscountStrategy(DiscountStrategy):
    """Calculate discount based on promotional code."""

    def calculate_discount(
        self,
        promotion: Optional['Promotion'],
        subtotal: float,
        order_items: list['OrderItem'],
        products: dict[int, 'Product']
    ) -> float:
        """
        Calculate promotional discount rate.

        Args:
            promotion: Promotion object (or None)
            subtotal: Current subtotal for validation
            order_items: List of order items
            products: Dictionary of products

        Returns:
            Discount rate (0.0 to 1.0, e.g., 0.15 for 15%)
        """
        if not promotion:
            return 0.0

        # Check if promotion is still valid
        if datetime.datetime.now() > promotion.valid_until:
            return 0.0

        # Check minimum purchase requirement
        if subtotal < promotion.min_purchase.value:
            return 0.0

        # Check if any items match promo category
        applicable = False
        for item in order_items:
            product = products.get(item.product_id)
            if product:
                if promotion.category == 'all' or product.category == promotion.category:
                    applicable = True
                    break

        if applicable:
            return promotion.discount_percent / 100

        return 0.0
