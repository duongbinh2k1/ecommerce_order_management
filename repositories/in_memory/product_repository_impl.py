"""
In-memory implementation of ProductRepository
Replaces global 'products' dictionary with proper repository pattern
"""
from domain.models.product import Product
from repositories.in_memory.base_repository import InMemoryRepositoryBase


class InMemoryProductRepository(InMemoryRepositoryBase[Product]):
    """
    In-memory storage for products.
    Implements ProductRepository interface by inheriting common CRUD from base.
    """
    pass  # All methods inherited from InMemoryRepositoryBase[Product]
