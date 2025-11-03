"""
Payment method enum - extracted from payment_info type validation
Used in: process_order() for payment validation, Order.payment_method
"""
from enum import Enum


class PaymentMethod(Enum):
    CREDIT_CARD = 'credit_card'
    PAYPAL = 'paypal'
