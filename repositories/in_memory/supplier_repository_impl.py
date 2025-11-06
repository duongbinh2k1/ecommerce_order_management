"""
In-memory implementation of SupplierRepository
Replaces global 'suppliers' dictionary
"""
from domain.models.supplier import Supplier
from repositories.in_memory.base_repository import InMemoryRepositoryBase


class InMemorySupplierRepository(InMemoryRepositoryBase[Supplier]):
    """In-memory storage for suppliers"""
    pass  # All methods inherited from InMemoryRepositoryBase[Supplier]
