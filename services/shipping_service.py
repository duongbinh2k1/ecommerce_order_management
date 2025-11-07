"""Shipping Service - Handles shipping calculations and logistics."""

from typing import TYPE_CHECKING
from domain.enums.shipping_method import ShippingMethod
from domain.enums.membership_tier import MembershipTier
from repositories.interfaces.shipment_repository import ShipmentRepository

if TYPE_CHECKING:
    from domain.models.customer import Customer


class ShippingService:
    """Service for shipping cost calculations and shipment management."""

    def __init__(self, shipment_repository: ShipmentRepository) -> None:
        """
        Initialize the shipping service.
        
        Args:
            shipment_repository: Repository for shipment data access (DI)
        """
        self.__repository = shipment_repository

    def calculate_shipping_cost(
        self,
        shipping_method: ShippingMethod,
        total_weight: float,
        subtotal: float,
        customer_tier: MembershipTier
    ) -> float:
        """
        Calculate shipping cost based on method, weight, and customer tier.

        Args:
            shipping_method: Selected shipping method
            total_weight: Total package weight in kg
            subtotal: Order subtotal (for free shipping threshold)
            customer_tier: Customer's membership tier

        Returns:
            Shipping cost
        """
        shipping_cost = 0.0

        if shipping_method == ShippingMethod.EXPRESS:
            shipping_cost = 25 + (total_weight * 0.5)
            # Gold members get 50% off express shipping
            if customer_tier == MembershipTier.GOLD:
                shipping_cost *= 0.5

        elif shipping_method == ShippingMethod.STANDARD:
            if subtotal < 50:
                shipping_cost = 5 + (total_weight * 0.2)
            else:
                shipping_cost = 0  # Free shipping over $50

        elif shipping_method == ShippingMethod.OVERNIGHT:
            shipping_cost = 50 + (total_weight * 1.0)

        return shipping_cost

    def create_shipment(
        self,
        order_id: str,
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
        import random
        shipment_id = self.__repository.get_next_id()
        tracking_number = f"TRACK{order_id}{random.randint(1000, 9999)}"

        shipment = {
            'shipment_id': shipment_id,
            'order_id': order_id,
            'tracking_number': tracking_number,
            'shipping_method': shipping_method if isinstance(shipping_method, str) else shipping_method.value,
            'address': address,
            'status': 'pending'
        }
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
        # Find shipment by tracking number
        for shipment in self.__repository.get_all().values():
            if shipment.get('tracking_number') == tracking_number:
                shipment['status'] = new_status
                self.__repository.update(shipment)
                return True
        return False

    def get_tracking_info(self, tracking_number: str) -> dict:
        """
        Get shipment tracking information.

        Args:
            tracking_number: Tracking number

        Returns:
            Tracking information dictionary or empty dict if not found
        """
        # Find shipment by tracking number
        for shipment in self.__repository.get_all().values():
            if shipment.get('tracking_number') == tracking_number:
                return shipment
        return {}
