"""Promotion Service - Manages promotional campaigns."""

from typing import Optional
import datetime
from domain.models.promotion import Promotion


class PromotionService:
    """Service for promotion and discount code management."""

    def __init__(self) -> None:
        """Initialize the promotion service."""
        self.__promotions: dict[str, Promotion] = {}

    def add_promotion(
        self,
        promo_id: str,
        code: str,
        discount: float,
        min_purchase: float,
        valid_until: datetime.datetime,
        category: str
    ) -> Promotion:
        """
        Add a new promotion code.

        Args:
            promo_id: Unique promotion identifier
            code: Promotion code string
            discount: Discount percentage
            min_purchase: Minimum purchase amount
            valid_until: Expiration datetime
            category: Applicable category ('all' or specific)

        Returns:
            The created Promotion instance
        """
        promotion = Promotion(
            promo_id=promo_id,
            code=code,
            discount_percent=discount,
            min_purchase=min_purchase,
            valid_until=valid_until,
            category=category
        )
        self.__promotions[code] = promotion
        return promotion

    def get_promotion(self, code: str) -> Optional[Promotion]:
        """
        Get a promotion by code.

        Args:
            code: Promotion code

        Returns:
            Promotion if found and valid, None otherwise
        """
        promotion = self.__promotions.get(code)
        
        # Check if promotion is still valid
        if promotion and datetime.datetime.now() > promotion.valid_until:
            return None
            
        return promotion

    def increment_usage(self, code: str) -> bool:
        """
        Increment promotion usage count.

        Args:
            code: Promotion code

        Returns:
            True if successful
        """
        promotion = self.__promotions.get(code)
        if promotion:
            promotion.used_count += 1
            return True
        return False

    def get_active_promotions(self) -> list[Promotion]:
        """
        Get all currently active promotions.

        Returns:
            List of active promotions
        """
        now = datetime.datetime.now()
        return [
            promo for promo in self.__promotions.values()
            if promo.valid_until > now
        ]

    def get_all_promotions(self) -> dict[str, Promotion]:
        """
        Get all promotions.

        Returns:
            Dictionary of all promotions
        """
        return self.__promotions.copy()
