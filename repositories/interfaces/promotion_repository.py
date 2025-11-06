"""
Promotion Repository Interface - defines contract for promotion data access
"""
from typing import Protocol, Optional
from domain.models.promotion import Promotion


class PromotionRepository(Protocol):
    """Interface for promotion data access"""
    
    def add(self, promotion: Promotion) -> None:
        """Add a new promotion"""
        ...
    
    def get(self, promo_code: str) -> Optional[Promotion]:
        """Retrieve a promotion by code"""
        ...
    
    def update(self, promotion: Promotion) -> None:
        """Update an existing promotion"""
        ...
    
    def delete(self, promo_code: str) -> None:
        """Remove a promotion"""
        ...
    
    def get_all(self) -> dict[str, Promotion]:
        """Get all promotions"""
        ...
    
    def exists(self, promo_code: str) -> bool:
        """Check if a promotion exists"""
        ...
