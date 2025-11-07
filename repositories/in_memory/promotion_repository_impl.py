"""
In-memory implementation of PromotionRepository
Replaces global 'promotions' dictionary
"""
from typing import Optional
from domain.models.promotion import Promotion


class InMemoryPromotionRepository:
    """In-memory storage for promotions"""

    def __init__(self) -> None:
        """Initialize with empty storage"""
        self._storage: dict[int, Promotion] = {}

    def add(self, promotion: Promotion) -> None:
        """Add a new promotion to the repository"""
        self._storage[promotion.code] = promotion

    def get(self, promo_code: int) -> Optional[Promotion]:
        """Retrieve a promotion by code"""
        return self._storage.get(promo_code)

    def update(self, promotion: Promotion) -> None:
        """Update an existing promotion"""
        self._storage[promotion.code] = promotion

    def delete(self, promo_code: int) -> None:
        """Remove a promotion from the repository"""
        if promo_code in self._storage:
            del self._storage[promo_code]

    def get_all(self) -> dict[int, Promotion]:
        """Get all promotions"""
        return self._storage.copy()

    def exists(self, promo_code: int) -> bool:
        """Check if a promotion exists"""
        return promo_code in self._storage
