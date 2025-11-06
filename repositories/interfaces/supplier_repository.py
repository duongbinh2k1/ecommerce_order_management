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
    
    def get(self, supplier_id: str) -> Optional[Supplier]:
        """Retrieve a supplier by ID"""
        ...
    
    def update(self, supplier: Supplier) -> None:
        """Update an existing supplier"""
        ...
    
    def delete(self, supplier_id: str) -> None:
        """Remove a supplier"""
        ...
    
    def get_all(self) -> dict[str, Supplier]:
        """Get all suppliers"""
        ...
    
    def exists(self, supplier_id: str) -> bool:
        """Check if a supplier exists"""
        ...
