"""
Customer segment enum - extracted from hardcoded segment strings and marketing logic
Used in: send_marketing_email() for customer segmentation
"""
from enum import StrEnum


class CustomerSegment(StrEnum):
    ALL = 'all'
    GOLD = 'gold'
    INACTIVE = 'inactive'
