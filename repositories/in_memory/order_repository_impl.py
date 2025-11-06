"""
In-memory implementation of OrderRepository
Replaces global 'orders' dictionary and 'next_order_id' counter
"""
from domain.models.order import Order
from repositories.in_memory.base_repository import InMemoryRepositoryBase


class InMemoryOrderRepository(InMemoryRepositoryBase[Order]):
    """
    In-memory storage for orders.
    Extends base with order ID generation.
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.__next_id: int = 1000  # Start from 1000 like original
    
    def get_next_id(self) -> int:
        """Get next available order ID"""
        current_id = self.__next_id
        self.__next_id += 1
        return current_id
