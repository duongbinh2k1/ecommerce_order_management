"""
Phone number value object - extracted from Customer.phone
Used in: Customer
"""
from typing import Optional


class PhoneNumber:
    def __init__(self, phone: Optional[str]) -> None:
        self.__phone = phone

    @property
    def value(self) -> Optional[str]:
        """Get the phone number string value"""
        return self.__phone

    def __str__(self) -> str:
        return self.__phone if self.__phone else ""

    def __repr__(self) -> str:
        return f"PhoneNumber('{self.__phone}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PhoneNumber):
            return self.__phone == other.value
        return False

    def __bool__(self) -> bool:
        """Allow truthiness check like 'if customer.phone:'"""
        return bool(self.__phone)

    def __hash__(self) -> int:
        return hash(self.__phone)
