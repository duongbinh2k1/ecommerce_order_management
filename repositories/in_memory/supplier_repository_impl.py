"""
In-memory implementation of SupplierRepository
Replaces global 'suppliers' dictionary
"""
from typing import Optional
from domain.models.supplier import Supplier


class InMemorySupplierRepository:
    """In-memory storage for suppliers"""

    def __init__(self) -> None:
        """Initialize with empty storage"""
        self._storage: dict[int, Supplier] = {
        }  # Internal storage uses int keys

    def add(self, supplier: Supplier) -> None:
        """Add a new supplier to the repository"""
        self._storage[supplier.supplier_id] = supplier

    def get(self, supplier_id: int) -> Optional[Supplier]:
        """Retrieve a supplier by ID"""
        return self._storage.get(supplier_id)

    def update(self, supplier: Supplier) -> None:
        """Update an existing supplier"""
        self._storage[supplier.supplier_id] = supplier

    def delete(self, supplier_id: int) -> None:
        """Remove a supplier from the repository"""
        if supplier_id in self._storage:
            del self._storage[supplier_id]

    def get_all(self) -> dict[int, Supplier]:
        """Get all suppliers"""
        return self._storage.copy()

    def exists(self, supplier_id: int) -> bool:
        """Check if a supplier exists"""
        return supplier_id in self._storage
