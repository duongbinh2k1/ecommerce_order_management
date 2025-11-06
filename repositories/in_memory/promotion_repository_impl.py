"""
In-memory implementation of PromotionRepository
Replaces global 'promotions' dictionary
"""
from domain.models.promotion import Promotion
from repositories.in_memory.base_repository import InMemoryRepositoryBase


class InMemoryPromotionRepository(InMemoryRepositoryBase[Promotion]):
    """In-memory storage for promotions"""
    pass  # All methods inherited from InMemoryRepositoryBase[Promotion]
