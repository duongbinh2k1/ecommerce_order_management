"""Pricing Service - Coordinates all discount strategies."""

from typing import Optional, TYPE_CHECKING
from domain.value_objects.money import Money
from domain.value_objects.pricing_result import PricingResult
from services.pricing.strategies import (
    MembershipDiscountStrategy,
    PromotionalDiscountStrategy,
    BulkDiscountStrategy,
    LoyaltyDiscountStrategy
)

if TYPE_CHECKING:
    from domain.models.customer import Customer
    from domain.models.order_item import OrderItem
    from domain.models.promotion import Promotion
    from domain.models.product import Product


class PricingService:
    """Service for pricing and discount calculations."""

    def __init__(
        self,
        membership_strategy: MembershipDiscountStrategy,
        promotional_strategy: PromotionalDiscountStrategy,
        bulk_strategy: BulkDiscountStrategy,
        loyalty_strategy: LoyaltyDiscountStrategy
    ) -> None:
        """Initialize pricing service with injected discount strategies."""
        self.__membership_strategy = membership_strategy
        self.__promotional_strategy = promotional_strategy
        self.__bulk_strategy = bulk_strategy
        self.__loyalty_strategy = loyalty_strategy

    def calculate_subtotal(
        self,
        order_items: list['OrderItem'],
        products: dict[int, 'Product']
    ) -> tuple[float, float]:
        """
        Calculate order subtotal and total weight.

        Args:
            order_items: List of order items
            products: Dictionary of products

        Returns:
            Tuple of (subtotal, total_weight)
        """
        subtotal = 0.0
        total_weight = 0.0

        for item in order_items:
            product = products.get(item.product_id)
            if product:
                item_price = item.unit_price.value if isinstance(
                    item.unit_price, Money) else item.unit_price
                subtotal += item.quantity * item_price
                total_weight += product.weight * item.quantity

        return subtotal, total_weight

    def apply_all_discounts(
        self,
        customer: 'Customer',
        order_items: list['OrderItem'],
        products: dict[int, 'Product'],
        promotion: Optional['Promotion'] = None
    ) -> PricingResult:
        """
        Apply all discount strategies and return pricing breakdown.
        
        Note: Each strategy handles its own multiplicative/additive logic internally
        to match legacy system behavior.

        Args:
            customer: Customer placing the order
            order_items: List of order items
            products: Dictionary of products
            promotion: Optional promotion code

        Returns:
            PricingResult with pricing breakdown
        """
        subtotal, total_weight = self.calculate_subtotal(order_items, products)

        # Apply membership discount
        membership_discount = self.__membership_strategy.calculate_discount(
            tier=customer.membership_tier,
            subtotal=subtotal
        )
        subtotal_after_membership = subtotal - membership_discount

        # Apply promotional discount
        promo_discount = self.__promotional_strategy.calculate_discount(
            promotion=promotion,
            original_subtotal=subtotal,
            current_subtotal=subtotal_after_membership,
            order_items=order_items,
            products=products
        )
        subtotal_after_promo = subtotal_after_membership - promo_discount

        # Apply bulk discount
        total_items = sum(item.quantity for item in order_items)
        bulk_discount = self.__bulk_strategy.calculate_discount(
            total_items=total_items,
            current_subtotal=subtotal_after_promo
        )
        subtotal_after_bulk = subtotal_after_promo - bulk_discount

        # Apply loyalty points discount (additive like legacy)
        loyalty_discount = self.__loyalty_strategy.calculate_discount(
            loyalty_points=customer.loyalty_points,
            current_subtotal=subtotal_after_bulk
        )
        final_price = subtotal_after_bulk - loyalty_discount
        points_used = self.__loyalty_strategy.calculate_points_used(loyalty_discount)

        return PricingResult(
            original_subtotal=subtotal,
            loyalty_points_used=points_used,
            subtotal_after_loyalty=final_price,
            total_weight=total_weight
        )

    def calculate_additional_discount(
        self,
        current_price: float,
        discount_percent: float
    ) -> float:
        """
        Calculate additional manual discount.

        Args:
            current_price: Current order price
            discount_percent: Discount percentage (0-100)

        Returns:
            New price after discount
        """
        discount_amount = current_price * (discount_percent / 100)
        return current_price - discount_amount
