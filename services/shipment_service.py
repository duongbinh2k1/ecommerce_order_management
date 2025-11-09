"""Shipment Service - Handles shipment lifecycle and tracking."""

from typing import Optional, List
from domain.enums.shipping_method import ShippingMethod
from domain.enums.shipment_status import ShipmentStatus
from domain.models.shipment import Shipment
from repositories.interfaces.shipment_repository import ShipmentRepository
import random

class ShipmentService:
    """Service for shipment management operations."""

    def __init__(self, shipment_repository: ShipmentRepository) -> None:
        """
        Initialize the shipment service.
        
        Args:
            shipment_repository: Repository for shipment data access (DI)
        """
        self.__repository = shipment_repository

    def create_shipment(
        self,
        order_id: int,
        shipping_method: ShippingMethod,
        address: str
    ) -> str:
        """
        Create a new shipment and generate tracking number.

        Args:
            order_id: Order identifier
            shipping_method: Shipping method
            address: Delivery address

        Returns:
            Tracking number
        """
        shipment_id = self.__repository.get_next_id()
        tracking_number = f"TRACK{order_id}{random.randint(1000, 9999)}"

        shipment = Shipment(
            shipment_id=shipment_id,
            order_id=order_id,
            tracking_number=tracking_number,
            shipping_method=shipping_method.value,
            address=address,
            status=ShipmentStatus.PENDING.value
        )
        self.__repository.add(shipment)

        return tracking_number

    def update_shipment_status(
        self,
        tracking_number: str,
        new_status: str
    ) -> bool:
        """
        Update shipment status.

        Args:
            tracking_number: Tracking number
            new_status: New status (e.g., 'in_transit', 'delivered')

        Returns:
            True if successful, False if tracking number not found
        """
        shipment = self.__repository.find_by_tracking_number(tracking_number)
        if shipment:
            shipment.status = new_status
            self.__repository.update(shipment)
            return True
        return False

    def get_tracking_info(self, tracking_number: str) -> Optional[Shipment]:
        """
        Get shipment tracking information.

        Args:
            tracking_number: Tracking number

        Returns:
            Shipment object or None if not found
        """
        return self.__repository.find_by_tracking_number(tracking_number)

    def get_shipments_by_order(self, order_id: int) -> List[Shipment]:
        """
        Get all shipments for a specific order.

        Args:
            order_id: Order identifier

        Returns:
            List of shipments for the order
        """
        return self.__repository.find_by_order_id(order_id)

    def get_all_shipments(self) -> List[Shipment]:
        """Get all shipments."""
        return self.__repository.get_all()

    def ship_order(
        self,
        order_id: int,
        shipping_method: ShippingMethod,
        address: str
    ) -> str:
        """
        Ship an order by creating shipment and updating status.

        Args:
            order_id: Order identifier
            shipping_method: Selected shipping method
            address: Delivery address

        Returns:
            Tracking number
        """
        # Create shipment
        tracking_number = self.create_shipment(
            order_id=order_id,
            shipping_method=shipping_method,
            address=address
        )

        # Update status to in_transit
        self.update_shipment_status(tracking_number, ShipmentStatus.IN_TRANSIT.value)

        return tracking_number

    def cancel_shipment(self, tracking_number: str) -> bool:
        """
        Cancel a shipment if it's still pending.

        Args:
            tracking_number: Tracking number

        Returns:
            True if cancelled successfully, False otherwise
        """
        shipment = self.__repository.find_by_tracking_number(tracking_number)
        if shipment and shipment.status == ShipmentStatus.PENDING:
            shipment.status = ShipmentStatus.CANCELLED.value
            self.__repository.update(shipment)
            return True
        return False

    def mark_delivered(self, tracking_number: str) -> bool:
        """
        Mark shipment as delivered.

        Args:
            tracking_number: Tracking number

        Returns:
            True if marked successfully, False otherwise
        """
        return self.update_shipment_status(tracking_number, ShipmentStatus.DELIVERED.value)