"""
Repository interface definitions using Protocols (PEP 544)
These define contracts for data access without concrete implementations
"""
from repositories.interfaces.product_repository import ProductRepository
from repositories.interfaces.customer_repository import CustomerRepository
from repositories.interfaces.order_repository import OrderRepository
from repositories.interfaces.supplier_repository import SupplierRepository
from repositories.interfaces.promotion_repository import PromotionRepository
from repositories.interfaces.shipment_repository import ShipmentRepository

__all__ = [
    'ProductRepository',
    'CustomerRepository',
    'OrderRepository',
    'SupplierRepository',
    'PromotionRepository',
    'ShipmentRepository',
]
