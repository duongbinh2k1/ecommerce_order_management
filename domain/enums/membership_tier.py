"""
Membership tier enum - extracted from hardcoded tier strings and discount logic
Used in: Customer.membership_tier, process_order() for discounts
"""
from enum import StrEnum


class MembershipTier(StrEnum):
    STANDARD = 'standard'
    BRONZE = 'bronze'
    SILVER = 'silver'
    GOLD = 'gold'
    SUSPENDED = 'suspended'
