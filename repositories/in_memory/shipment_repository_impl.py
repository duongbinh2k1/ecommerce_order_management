"""
In-memory implementation of ShipmentRepository
Replaces global 'shipments' dictionary and 'next_shipment_id' counter
"""
from typing import Any, Optional


class InMemoryShipmentRepository:
    """In-memory storage for shipments"""

    def __init__(self) -> None:
        self.__shipments: dict[int, dict[str, Any]] = {}
        self.__next_id: int = 1

    def add(self, shipment: dict[str, Any]) -> None:
        """Add a new shipment"""
        self.__shipments[shipment['shipment_id']] = shipment

    def get(self, shipment_id: int) -> Optional[dict[str, Any]]:
        """Retrieve a shipment by ID"""
        return self.__shipments.get(shipment_id)

    def update(self, shipment: dict[str, Any]) -> None:
        """Update an existing shipment"""
        self.__shipments[shipment['shipment_id']] = shipment

    def delete(self, shipment_id: int) -> None:
        """Remove a shipment"""
        if shipment_id in self.__shipments:
            del self.__shipments[shipment_id]

    def get_all(self) -> dict[int, dict[str, Any]]:
        """Get all shipments"""
        return self.__shipments.copy()

    def exists(self, shipment_id: int) -> bool:
        """Check if a shipment exists"""
        return shipment_id in self.__shipments

    def get_next_id(self) -> int:
        """Get next available shipment ID"""
        current_id = self.__next_id
        self.__next_id += 1
        return current_id
