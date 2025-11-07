"""
Shipment Repository Interface - defines contract for shipment data access
Note: Shipment is dict-based (not a domain model yet)
"""
from typing import Protocol, Optional


class ShipmentRepository(Protocol):
    """
    Interface for shipment data access.
    Note: Uses dict instead of domain model (legacy compatibility).
    """

    def add(self, shipment: dict) -> None:
        """Add a new shipment"""
        ...

    def get(self, shipment_id: str) -> Optional[dict]:
        """Retrieve a shipment by ID"""
        ...

    def update(self, shipment: dict) -> None:
        """Update an existing shipment"""
        ...

    def delete(self, shipment_id: str) -> None:
        """Remove a shipment"""
        ...

    def get_all(self) -> dict[str, dict]:
        """Get all shipments"""
        ...

    def exists(self, shipment_id: str) -> bool:
        """Check if a shipment exists"""
        ...

    def get_next_id(self) -> int:
        """Get next available shipment ID"""
        ...
