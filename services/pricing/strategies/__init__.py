"""Discount strategies package - Strategy Pattern implementation."""

from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from domain.models.customer import Customer
    from domain.models.order_item import OrderItem
    from domain.models.promotion import Promotion
    from domain.models.product import Product
    from domain.enums.membership_tier import MembershipTier


class MembershipDiscountStrategy(Protocol):
    """Strategy for membership-based discounts."""
    
    def calculate_discount(self, tier: 'MembershipTier', subtotal: float) -> float:
        """Calculate membership discount amount."""
        ...


class BulkDiscountStrategy(Protocol):
    """Strategy for bulk purchase discounts."""
    
    def calculate_discount(self, total_items: int, current_subtotal: float) -> float:
        """Calculate bulk discount amount to subtract from current_subtotal."""
        ...


class PromotionalDiscountStrategy(Protocol):
    """Strategy for promotional code discounts."""
    
    def calculate_discount(
        self, 
        promotion: Optional['Promotion'],
        original_subtotal: float,
        current_subtotal: float,  # After membership discount
        order_items: list['OrderItem'], 
        products: dict[int, 'Product']
    ) -> float:
        """Calculate promotional discount amount to subtract from current_subtotal."""
        ...


class LoyaltyDiscountStrategy(Protocol):
    """Strategy for loyalty points discounts."""
    
    def calculate_discount(self, loyalty_points: int, current_subtotal: float) -> float:
        """Calculate loyalty discount amount."""
        ...
    
    def calculate_points_used(self, discount_amount: float) -> int:
        """Calculate points used for discount amount."""
        ...


# Import all strategies for easy access
from services.pricing.strategies.membership_discount import MembershipDiscountStrategyImpl
from services.pricing.strategies.promotional_discount import PromotionalDiscountStrategyImpl
from services.pricing.strategies.bulk_discount import BulkDiscountStrategyImpl
from services.pricing.strategies.loyalty_discount import LoyaltyDiscountStrategyImpl

__all__ = [
    'MembershipDiscountStrategy',
    'BulkDiscountStrategy', 
    'PromotionalDiscountStrategy',
    'LoyaltyDiscountStrategy',
    'MembershipDiscountStrategyImpl',
    'PromotionalDiscountStrategyImpl',
    'BulkDiscountStrategyImpl',
    'LoyaltyDiscountStrategyImpl'
]
