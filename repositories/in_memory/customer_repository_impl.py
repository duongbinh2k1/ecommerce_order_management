"""
In-memory implementation of CustomerRepository
Replaces global 'customers' dictionary
"""
from domain.models.customer import Customer
from repositories.in_memory.base_repository import InMemoryRepositoryBase


class InMemoryCustomerRepository(InMemoryRepositoryBase[Customer]):
    """In-memory storage for customers"""
    pass  # All methods inherited from InMemoryRepositoryBase[Customer]
