"""Discount strategies package - Strategy Pattern implementation."""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract base class for discount strategies (Open/Closed Principle)."""

    @abstractmethod
    def calculate_discount(self, *args, **kwargs):
        """
        Calculate discount amount.

        Returns:
            Discount amount (0 or positive float) or tuple for loyalty
        """
        raise NotImplementedError


# Import all strategies for easy access
from services.pricing.strategies.membership_discount import MembershipDiscountStrategy
from services.pricing.strategies.promotional_discount import PromotionalDiscountStrategy
from services.pricing.strategies.bulk_discount import BulkDiscountStrategy
from services.pricing.strategies.loyalty_discount import LoyaltyPointsDiscountStrategy

__all__ = [
    'DiscountStrategy',
    'MembershipDiscountStrategy',
    'PromotionalDiscountStrategy',
    'BulkDiscountStrategy',
    'LoyaltyPointsDiscountStrategy'
]
