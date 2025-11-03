"""
Order status enum - extracted from hardcoded strings in order_system.py
Used in: Order.status, update_order_status(), cancel_order()
"""
from enum import Enum


class OrderStatus(Enum):
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    IN_TRANSIT = 'in_transit'  # Used in shipment tracking
