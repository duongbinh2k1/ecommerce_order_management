"""
Shipment status enum - for tracking package delivery status
Used in: ShippingService for shipment status updates
"""
from enum import StrEnum


class ShipmentStatus(StrEnum):
    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    RETURNED = 'returned'