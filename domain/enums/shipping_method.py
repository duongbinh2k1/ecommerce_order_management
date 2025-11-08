"""
Shipping method enum - extracted from hardcoded shipping_method strings
Used in: process_order() for shipping cost calculation
"""
from enum import StrEnum


class ShippingMethod(StrEnum):
    STANDARD = 'standard'
    EXPRESS = 'express'
    OVERNIGHT = 'overnight'
