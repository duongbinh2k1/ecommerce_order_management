"""
In-memory implementation of ProductRepository
Replaces global 'products' dictionary with proper repository pattern
"""
from typing import Optional
from domain.models.product import Product


class InMemoryProductRepository:
    """
    In-memory storage for products.
    Implements ProductRepository Protocol.
    """

    def __init__(self) -> None:
        """Initialize with empty storage"""
        self._storage: dict[int, Product] = {
        }  # Internal storage uses int keys

    def add(self, product: Product) -> None:
        """Add a new product to the repository"""
        self._storage[product.product_id] = product

    def get(self, product_id: int) -> Optional[Product]:
        """Retrieve a product by ID"""
        return self._storage.get(product_id)

    def update(self, product: Product) -> None:
        """Update an existing product"""
        self._storage[product.product_id] = product

    def delete(self, product_id: int) -> None:
        """Remove a product from the repository"""
        if product_id in self._storage:
            del self._storage[product_id]

    def get_all(self) -> dict[int, Product]:
        """Get all products"""
        return self._storage.copy()

    def exists(self, product_id: int) -> bool:
        """Check if a product exists"""
        return product_id in self._storage
