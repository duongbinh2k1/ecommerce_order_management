"""
Order Repository Interface - defines contract for order data access
"""
from typing import Protocol, Optional
from domain.models.order import Order


class OrderRepository(Protocol):
    """Interface for order data access"""

    def add(self, order: Order) -> None:
        """Add a new order"""
        ...

    def get(self, order_id: int) -> Optional[Order]:
        """Retrieve an order by ID"""
        ...

    def update(self, order: Order) -> None:
        """Update an existing order"""
        ...

    def delete(self, order_id: int) -> None:
        """Remove an order"""
        ...

    def get_all(self) -> dict[int, Order]:
        """Get all orders"""
        ...

    def exists(self, order_id: int) -> bool:
        """Check if an order exists"""
        ...

    def get_next_id(self) -> int:
        """Get next available order ID"""
        ...
