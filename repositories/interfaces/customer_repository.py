"""
Customer Repository Interface - defines contract for customer data access
"""
from typing import Protocol, Optional
from domain.models.customer import Customer


class CustomerRepository(Protocol):
    """Interface for customer data access"""

    def add(self, customer: Customer) -> None:
        """Add a new customer"""
        ...

    def get(self, customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by ID"""
        ...

    def update(self, customer: Customer) -> None:
        """Update an existing customer"""
        ...

    def delete(self, customer_id: int) -> None:
        """Remove a customer"""
        ...

    def get_all(self) -> dict[int, Customer]:
        """Get all customers"""
        ...

    def exists(self, customer_id: str) -> bool:
        """Check if a customer exists"""
        ...
