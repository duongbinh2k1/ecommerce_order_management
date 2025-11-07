"""
Application layer - Orchestrates services and handles dependency injection
"""
from .order_processor import OrderProcessor

__all__ = [
    'OrderProcessor'
]
