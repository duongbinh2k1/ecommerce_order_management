"""
In-memory repository implementations
These replace global dictionaries with proper data access layer
"""
from repositories.in_memory.product_repository_impl import InMemoryProductRepository
from repositories.in_memory.customer_repository_impl import InMemoryCustomerRepository
from repositories.in_memory.order_repository_impl import InMemoryOrderRepository
from repositories.in_memory.supplier_repository_impl import InMemorySupplierRepository
from repositories.in_memory.promotion_repository_impl import InMemoryPromotionRepository
from repositories.in_memory.shipment_repository_impl import InMemoryShipmentRepository

__all__ = [
    'InMemoryProductRepository',
    'InMemoryCustomerRepository',
    'InMemoryOrderRepository',
    'InMemorySupplierRepository',
    'InMemoryPromotionRepository',
    'InMemoryShipmentRepository',
]
