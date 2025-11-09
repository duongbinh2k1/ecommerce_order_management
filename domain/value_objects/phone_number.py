"""
Phone number value object - extracted from Customer.phone
Used in: Customer
"""
from typing import Optional


class PhoneNumber:
    def __init__(self, phone: Optional[str]) -> None:
        self.__validate(phone)
        self.__phone = phone

    def __validate(self, phone: Optional[str]) -> None:
        """Validate phone number format"""
        if phone is not None:
            # Remove spaces and common separators for validation
            cleaned_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
            if not cleaned_phone.isdigit() or len(cleaned_phone) < 5:
                raise ValueError(f"Invalid phone number: {phone}")
            if len(cleaned_phone) > 15:  # Max international phone number length
                raise ValueError(f"Phone number too long: {phone}")

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
