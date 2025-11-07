"""
Shipment Repository Interface - defines contract for shipment data access
Note: Shipment is dict-based (not a domain model yet)
"""
from typing import Any, Protocol, Optional


class ShipmentRepository(Protocol):
    """
    Interface for shipment data access.
    Note: Uses dict instead of domain model (legacy compatibility).
    """

    def add(self, shipment: dict[str, Any]) -> None:
        """Add a new shipment"""
        ...

    def get(self, shipment_id: int) -> Optional[dict[str, Any]]:
        """Retrieve a shipment by ID"""
        ...

    def update(self, shipment: dict[str, Any]) -> None:
        """Update an existing shipment"""
        ...

    def delete(self, shipment_id: int) -> None:
        """Remove a shipment"""
        ...

    def get_all(self) -> dict[int, dict[str, Any]]:
        """Get all shipments"""
        ...

    def exists(self, shipment_id: int) -> bool:
        """Check if a shipment exists"""
        ...

    def get_next_id(self) -> int:
        """Get next available shipment ID"""
        ...
