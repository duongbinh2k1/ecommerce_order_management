"""
US State enum - for state abbreviations used in tax calculations
Used in: tax rate calculation logic from legacy system
"""
from enum import StrEnum


class USState(StrEnum):
    """US State abbreviations for tax calculation"""
    CA = 'CA'  # California - tax rate 0.0725
    NY = 'NY'  # New York - tax rate 0.04  
    TX = 'TX'  # Texas - tax rate 0.0625
    # Default tax rate 0.08 for other states