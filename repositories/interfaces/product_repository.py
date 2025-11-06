"""
Product Repository Interface - defines contract for product data access
Follows Repository Pattern and Dependency Inversion Principle
"""
from typing import Protocol, Optional
from domain.models.product import Product


class ProductRepository(Protocol):
    """
    Interface for product data access.
    Services depend on this abstraction, not concrete implementations.
    """
    
    def add(self, product: Product) -> None:
        """Add a new product to the repository"""
        ...
    
    def get(self, product_id: str) -> Optional[Product]:
        """Retrieve a product by ID"""
        ...
    
    def update(self, product: Product) -> None:
        """Update an existing product"""
        ...
    
    def delete(self, product_id: str) -> None:
        """Remove a product from the repository"""
        ...
    
    def get_all(self) -> dict[str, Product]:
        """Get all products"""
        ...
    
    def exists(self, product_id: str) -> bool:
        """Check if a product exists"""
        ...
