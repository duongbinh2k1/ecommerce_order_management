"""
In-memory implementation of ShipmentRepository
Replaces global 'shipments' dictionary and 'next_shipment_id' counter
"""
from typing import Optional, List
from domain.models.shipment import Shipment


class InMemoryShipmentRepository:
    """In-memory storage for shipments"""

    def __init__(self) -> None:
        self.__shipments: dict[int, Shipment] = {}
        self.__next_id: int = 1

    def add(self, shipment: Shipment) -> None:
        """Add a new shipment"""
        self.__shipments[shipment.shipment_id] = shipment

    def get(self, shipment_id: int) -> Optional[Shipment]:
        """Retrieve a shipment by ID"""
        return self.__shipments.get(shipment_id)

    def update(self, shipment: Shipment) -> None:
        """Update an existing shipment"""
        self.__shipments[shipment.shipment_id] = shipment

    def delete(self, shipment_id: int) -> None:
        """Remove a shipment"""
        if shipment_id in self.__shipments:
            del self.__shipments[shipment_id]

    def get_all(self) -> List[Shipment]:
        """Get all shipments"""
        return list(self.__shipments.values())

    def exists(self, shipment_id: int) -> bool:
        """Check if a shipment exists"""
        return shipment_id in self.__shipments

    def get_next_id(self) -> int:
        """Get next available shipment ID"""
        current_id = self.__next_id
        self.__next_id += 1
        return current_id

    def find_by_order_id(self, order_id: int) -> List[Shipment]:
        """Find shipments by order ID"""
        return [shipment for shipment in self.__shipments.values()
                if shipment.order_id == order_id]

    def find_by_tracking_number(self, tracking_number: str) -> Optional[Shipment]:
        """Find shipment by tracking number"""
        for shipment in self.__shipments.values():
            if shipment.tracking_number == tracking_number:
                return shipment
        return None
