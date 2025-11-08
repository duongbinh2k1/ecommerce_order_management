"""
Payment status enum - for tracking payment states
Used in: PaymentService for payment status management
"""
from enum import StrEnum


class PaymentStatus(StrEnum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'
    CANCELLED = 'cancelled'