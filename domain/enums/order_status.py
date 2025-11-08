"""
Order status enum - extracted from hardcoded strings in order_system.py
Used in: Order.status, update_order_status(), cancel_order()
"""
from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    IN_TRANSIT = 'in_transit'
