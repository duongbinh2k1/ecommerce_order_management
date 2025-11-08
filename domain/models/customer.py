"""
Customer model - moved from order_system.py
Added validation logic as per README requirements
"""
from typing import List, Optional
from domain.value_objects.email import Email
from domain.value_objects.phone_number import PhoneNumber
from domain.value_objects.address import Address
from domain.enums.membership_tier import MembershipTier


class Customer:
    def __init__(
        self,
        customer_id: int,
        name: str,
        email: str,
        membership_tier: MembershipTier,
        phone: str,
        address: str,
        loyalty_points: int,
        order_history: Optional[List[int]] = None
    ) -> None:
        self.__validate(name, loyalty_points)

        self.__customer_id: int = customer_id
        self.__name: str = name
        self.__email: Email = Email(email)
        self.__membership_tier: MembershipTier = membership_tier
        self.__phone: PhoneNumber = PhoneNumber(phone)
        self.__address: Address = Address(address)
        self.__loyalty_points: int = loyalty_points
        self.__order_history: List[int] = order_history if order_history is not None else []

    def __validate(self, name: str, loyalty_points: int) -> None:
        """Validate customer business rules"""
        if not name or not isinstance(name, str):
            raise ValueError("Customer name must be a non-empty string")
        if loyalty_points < 0:
            raise ValueError("Loyalty points cannot be negative")

    @property
    def customer_id(self) -> int:
        return self.__customer_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> Email:
        return self.__email

    @property
    def membership_tier(self) -> MembershipTier:
        return self.__membership_tier

    @membership_tier.setter
    def membership_tier(self, value: str) -> None:
        self.__membership_tier = MembershipTier(value)

    @property
    def phone(self) -> PhoneNumber:
        return self.__phone

    @property
    def address(self) -> Address:
        return self.__address

    @property
    def loyalty_points(self) -> int:
        return self.__loyalty_points

    @loyalty_points.setter
    def loyalty_points(self, value: int) -> None:
        if value < 0:
            raise ValueError("Loyalty points cannot be negative")
        self.__loyalty_points = value

    @property
    def order_history(self) -> List[int]:
        return self.__order_history

    @order_history.setter
    def order_history(self, value: List[int]) -> None:
        self.__order_history = value
