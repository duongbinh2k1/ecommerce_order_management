"""
In-memory implementation of CustomerRepository
Replaces global 'customers' dictionary
"""
from typing import Optional
from domain.models.customer import Customer


class InMemoryCustomerRepository:
    """In-memory storage for customers"""

    def __init__(self) -> None:
        """Initialize with empty storage"""
        self._storage: dict[int, Customer] = {
        }  # Internal storage uses int keys

    def add(self, customer: Customer) -> None:
        """Add a new customer to the repository"""
        self._storage[customer.customer_id] = customer

    def get(self, customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by ID"""
        return self._storage.get(customer_id)

    def update(self, customer: Customer) -> None:
        """Update an existing customer"""
        self._storage[customer.customer_id] = customer

    def delete(self, customer_id: int) -> None:
        """Remove a customer from the repository"""
        if customer_id in self._storage:
            del self._storage[customer_id]

    def get_all(self) -> dict[int, Customer]:
        """Get all customers"""
        return self._storage.copy()

    def exists(self, customer_id: int) -> bool:
        """Check if a customer exists"""
        return customer_id in self._storage
