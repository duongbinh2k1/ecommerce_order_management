"""
Supplier Repository Interface - defines contract for supplier data access
"""
from typing import Protocol, Optional
from domain.models.supplier import Supplier


class SupplierRepository(Protocol):
    """Interface for supplier data access"""

    def add(self, supplier: Supplier) -> None:
        """Add a new supplier"""
        ...

    def get(self, supplier_id: int) -> Optional[Supplier]:
        """Retrieve a supplier by ID"""
        ...

    def update(self, supplier: Supplier) -> None:
        """Update an existing supplier"""
        ...

    def delete(self, supplier_id: int) -> None:
        """Remove a supplier"""
        ...

    def get_all(self) -> dict[int, Supplier]:
        """Get all suppliers"""
        ...

    def exists(self, supplier_id: int) -> bool:
        """Check if a supplier exists"""
        ...
