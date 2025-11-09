"""
Product category enum - extracted from hardcoded category strings
Used in: Product.category, promotion category matching
"""
from enum import StrEnum


class ProductCategory(StrEnum):
    """Product categories for classification and promotion matching"""
    ELECTRONICS = 'Electronics'
    ACCESSORIES = 'Accessories' 
    FURNITURE = 'Furniture'
    ALL = 'all'  # Special category for promotions that apply to all categories