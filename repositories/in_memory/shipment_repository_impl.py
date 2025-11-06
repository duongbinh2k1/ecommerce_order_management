"""
In-memory implementation of ShipmentRepository
Replaces global 'shipments' dictionary and 'next_shipment_id' counter
"""
from typing import Optional


class InMemoryShipmentRepository:
    """In-memory storage for shipments"""
    
    def __init__(self) -> None:
        self.__shipments: dict[str, dict] = {}
        self.__next_id: int = 1  # Start from 1 like original
    
    def add(self, shipment: dict) -> None:
        """Add a new shipment"""
        self.__shipments[str(shipment['shipment_id'])] = shipment
    
    def get(self, shipment_id: str) -> Optional[dict]:
        """Retrieve a shipment by ID"""
        return self.__shipments.get(str(shipment_id))
    
    def update(self, shipment: dict) -> None:
        """Update an existing shipment"""
        self.__shipments[str(shipment['shipment_id'])] = shipment
    
    def delete(self, shipment_id: str) -> None:
        """Remove a shipment"""
        if str(shipment_id) in self.__shipments:
            del self.__shipments[str(shipment_id)]
    
    def get_all(self) -> dict[str, dict]:
        """Get all shipments"""
        return self.__shipments.copy()
    
    def exists(self, shipment_id: str) -> bool:
        """Check if a shipment exists"""
        return str(shipment_id) in self.__shipments
    
    def get_next_id(self) -> int:
        """Get next available shipment ID"""
        current_id = self.__next_id
        self.__next_id += 1
        return current_id
