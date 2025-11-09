"""
Inventory Log Entry value object - immutable inventory change record
Used by: InventoryService for inventory change tracking
"""
import datetime
from typing import Optional, Any


class InventoryLogEntry:
    """Value object representing an inventory change log entry."""
    
    def __init__(
        self,
        product_id: int,
        quantity_change: int,
        reason: str,
        timestamp: Optional[datetime.datetime] = None
    ) -> None:
        """
        Initialize inventory log entry.
        
        Args:
            product_id: Product identifier
            quantity_change: Quantity change (positive for stock in, negative for stock out)
            reason: Reason for inventory change (e.g., 'initial_stock', 'restock', 'sale')
            timestamp: When the change occurred (defaults to now)
        """
        self.__validate(product_id, quantity_change, reason)
        
        self.__product_id = product_id
        self.__quantity_change = quantity_change
        self.__reason = reason.strip()
        self.__timestamp = timestamp or datetime.datetime.now()

    def __validate(
        self,
        product_id: int,
        quantity_change: int,
        reason: str
    ) -> None:
        """Validate log entry data."""
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("Product ID must be a positive integer")
        
        if not isinstance(quantity_change, int):
            raise ValueError("Quantity change must be an integer")
        
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Reason must be a non-empty string")

    @property
    def product_id(self) -> int:
        """Get product ID."""
        return self.__product_id

    @property
    def quantity_change(self) -> int:
        """Get quantity change."""
        return self.__quantity_change

    @property
    def reason(self) -> str:
        """Get reason for inventory change."""
        return self.__reason

    @property
    def timestamp(self) -> datetime.datetime:
        """Get timestamp when change occurred."""
        return self.__timestamp

    def is_stock_increase(self) -> bool:
        """Check if this entry represents a stock increase."""
        return self.__quantity_change > 0

    def is_stock_decrease(self) -> bool:
        """Check if this entry represents a stock decrease."""
        return self.__quantity_change < 0

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary for backward compatibility.
        
        Returns:
            dict: Log entry data as dictionary (same format as legacy)
        """
        return {
            'product_id': self.__product_id,
            'quantity_change': self.__quantity_change,
            'reason': self.__reason,
            'timestamp': self.__timestamp
        }

    def __str__(self) -> str:
        """String representation of inventory log entry."""
        direction = "+" if self.__quantity_change >= 0 else ""
        return f"Product {self.__product_id}: {direction}{self.__quantity_change} ({self.__reason})"

    def __repr__(self) -> str:
        """Detailed representation of inventory log entry."""
        return (
            f"InventoryLogEntry("
            f"product_id={self.__product_id}, "
            f"quantity_change={self.__quantity_change}, "
            f"reason='{self.__reason}', "
            f"timestamp={self.__timestamp})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another inventory log entry."""
        if not isinstance(other, InventoryLogEntry):
            return False
        
        return (
            self.__product_id == other.product_id and
            self.__quantity_change == other.quantity_change and
            self.__reason == other.reason and
            self.__timestamp == other.timestamp
        )

    def __hash__(self) -> int:
        """Hash for using in sets/dicts."""
        return hash((
            self.__product_id,
            self.__quantity_change,
            self.__reason,
            self.__timestamp
        ))