"""Supplier Service - Manages supplier operations."""

from typing import Optional
from domain.models.supplier import Supplier
from repositories.interfaces.supplier_repository import SupplierRepository


class SupplierService:
    """Service for supplier management operations."""

    def __init__(self, supplier_repository: SupplierRepository) -> None:
        """
        Initialize the supplier service.
        
        Args:
            supplier_repository: Repository for supplier data access (DI)
        """
        self.__repository = supplier_repository

    def add_supplier(
        self,
        supplier_id: int,
        name: str,
        email: str,
        reliability: float
    ) -> Supplier:
        """
        Add a new supplier.

        Args:
            supplier_id: Unique supplier identifier
            name: Supplier name
            email: Supplier email address
            reliability: Reliability score (0-1)

        Returns:
            The created Supplier instance
        """
        supplier = Supplier(
            supplier_id=supplier_id,
            name=name,
            email=email,
            reliability_score=reliability
        )
        self.__repository.add(supplier)
        return supplier

    def get_supplier(self, supplier_id: int) -> Optional[Supplier]:
        """
        Retrieve a supplier by ID.

        Args:
            supplier_id: The supplier identifier

        Returns:
            The Supplier if found, None otherwise
        """
        return self.__repository.get(supplier_id)

    def get_reliable_suppliers(self, min_reliability: float = 0.7) -> list[Supplier]:
        """
        Get suppliers with reliability above threshold.

        Args:
            min_reliability: Minimum reliability threshold (default: 0.7)

        Returns:
            List of reliable suppliers
        """
        return [
            supplier for supplier in self.__repository.get_all().values()
            if supplier.reliability_score >= min_reliability
        ]

    def update_reliability(
        self,
        supplier_id: int,
        new_reliability: float
    ) -> bool:
        """
        Update supplier reliability score.

        Args:
            supplier_id: The supplier identifier
            new_reliability: New reliability score (0-1)

        Returns:
            True if successful, False if supplier not found
        """
        supplier = self.__repository.get(supplier_id)
        if not supplier:
            return False

        # Create updated supplier
        updated_supplier = Supplier(
            supplier_id=supplier.supplier_id,
            name=supplier.name,
            email=supplier.email.value,  # Extract primitive
            reliability_score=new_reliability
        )
        self.__repository.update(updated_supplier)
        return True

    def get_all_suppliers(self) -> dict[int, Supplier]:
        """
        Get all suppliers.

        Returns:
            Dictionary of all suppliers
        """
        return self.__repository.get_all()

    def notify_reorder(
        self,
        product_name: str,
        supplier_id: int,
        current_stock: int
    ) -> bool:
        """
        Notify supplier about low stock and need to reorder.

        Args:
            product_name: Name of the product
            supplier_id: Supplier identifier
            current_stock: Current stock level

        Returns:
            True if notification sent successfully
        """
        supplier = self.__repository.get(supplier_id)
        if not supplier:
            return False

        message = f"Low stock alert for {product_name}. Current stock: {current_stock}. Please prepare reorder."
        print(f"[EMAIL to {supplier.email.value}] {message}")
        return True
