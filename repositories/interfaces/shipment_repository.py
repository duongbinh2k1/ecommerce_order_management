"""
Shipment Repository Interface - defines contract for shipment data access
"""
from typing import Protocol, Optional, List
from domain.models.shipment import Shipment


class ShipmentRepository(Protocol):
    """
    Interface for shipment data access.
    """

    def add(self, shipment: Shipment) -> None:
        """Add a new shipment"""
        ...

    def get(self, shipment_id: int) -> Optional[Shipment]:
        """Retrieve a shipment by ID"""
        ...

    def update(self, shipment: Shipment) -> None:
        """Update an existing shipment"""
        ...

    def delete(self, shipment_id: int) -> None:
        """Remove a shipment"""
        ...

    def get_all(self) -> List[Shipment]:
        """Get all shipments"""
        ...

    def exists(self, shipment_id: int) -> bool:
        """Check if a shipment exists"""
        ...

    def get_next_id(self) -> int:
        """Get next available shipment ID"""
        ...

    def find_by_order_id(self, order_id: int) -> List[Shipment]:
        """Find shipments by order ID"""
        ...

    def find_by_tracking_number(self, tracking_number: str) -> Optional[Shipment]:
        """Find shipment by tracking number"""
        ...