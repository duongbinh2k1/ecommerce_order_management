"""
Shipment domain model - tracks package delivery
"""
from typing import Any
from domain.enums.shipment_status import ShipmentStatus
from domain.enums.shipping_method import ShippingMethod
from domain.value_objects.address import Address


class Shipment:
    def __init__(
        self,
        shipment_id: int,
        order_id: int,
        tracking_number: str,
        shipping_method: str,
        address: str,
        status: str = ShipmentStatus.PENDING
    ) -> None:
        self.__validate(shipment_id, order_id, tracking_number)

        self.__shipment_id: int = shipment_id
        self.__order_id: int = order_id
        self.__tracking_number: str = tracking_number
        self.__shipping_method: ShippingMethod = ShippingMethod(
            shipping_method)
        self.__address: Address = Address(address)
        self.__status: ShipmentStatus = ShipmentStatus(status)

    def __validate(self, shipment_id: int, order_id: int, tracking_number: str) -> None:
        if shipment_id <= 0:
            raise ValueError("Shipment ID must be positive")
        if order_id <= 0:
            raise ValueError("Order ID must be positive")
        if not tracking_number:
            raise ValueError("Tracking number cannot be empty")

    @property
    def shipment_id(self) -> int:
        return self.__shipment_id

    @property
    def order_id(self) -> int:
        return self.__order_id

    @property
    def tracking_number(self) -> str:
        return self.__tracking_number

    @property
    def shipping_method(self) -> ShippingMethod:
        return self.__shipping_method

    @property
    def address(self) -> Address:
        return self.__address

    @property
    def status(self) -> ShipmentStatus:
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        self.__status = ShipmentStatus(value)

    def __str__(self) -> str:
        return f"Shipment({self.__shipment_id}: {self.__tracking_number})"

    def __repr__(self) -> str:
        return f"Shipment(id={self.__shipment_id}, tracking='{self.__tracking_number}', status={self.__status.value})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Shipment):
            return False
        return self.__shipment_id == other.shipment_id

    def __hash__(self) -> int:
        return hash(self.__shipment_id)
