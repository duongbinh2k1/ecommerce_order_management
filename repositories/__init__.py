"""
Repository layer - Data access abstraction
Follows Repository Pattern and Dependency Inversion Principle
"""
from repositories.interfaces import (
    ProductRepository,
    CustomerRepository,
    OrderRepository,
    SupplierRepository,
    PromotionRepository,
    ShipmentRepository,
)

from repositories.in_memory import (
    InMemoryProductRepository,
    InMemoryCustomerRepository,
    InMemoryOrderRepository,
    InMemorySupplierRepository,
    InMemoryPromotionRepository,
    InMemoryShipmentRepository,
)

__all__ = [
    # Interfaces
    'ProductRepository',
    'CustomerRepository',
    'OrderRepository',
    'SupplierRepository',
    'PromotionRepository',
    'ShipmentRepository',
    # Implementations
    'InMemoryProductRepository',
    'InMemoryCustomerRepository',
    'InMemoryOrderRepository',
    'InMemorySupplierRepository',
    'InMemoryPromotionRepository',
    'InMemoryShipmentRepository',
]
