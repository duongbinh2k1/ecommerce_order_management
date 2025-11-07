"""
In-memory implementation of OrderRepository
Replaces global 'orders' dictionary and 'next_order_id' counter
"""
from typing import Optional
from domain.models.order import Order


class InMemoryOrderRepository:
    """
    In-memory storage for orders.
    Includes order ID generation.
    """

    def __init__(self) -> None:
        """Initialize with empty storage"""
        self._storage: dict[int, Order] = {
        }  # Internal storage uses int keys
        self.__next_id: int = 1  # Start from 1 like original

    def add(self, order: Order) -> None:
        """Add a new order to the repository"""
        self._storage[order.order_id] = order

    def get(self, order_id: int) -> Optional[Order]:
        """Retrieve an order by ID"""
        return self._storage.get(order_id)

    def update(self, order: Order) -> None:
        """Update an existing order"""
        self._storage[order.order_id] = order

    def delete(self, order_id: int) -> None:
        """Remove an order from the repository"""
        if order_id in self._storage:
            del self._storage[order_id]

    def get_all(self) -> dict[int, Order]:
        """Get all orders"""
        return self._storage.copy()

    def exists(self, order_id: int) -> bool:
        """Check if an order exists"""
        return order_id in self._storage

    def get_next_id(self) -> int:
        """Get next available order ID"""
        current_id = self.__next_id
        self.__next_id += 1
        return current_id
