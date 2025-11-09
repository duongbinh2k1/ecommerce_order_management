"""
Money value object - for all monetary values (price, total, discount, etc.)
Used throughout the system for financial calculations
"""
from typing import Union


class Money:
    def __init__(self, amount: Union[int, float]) -> None:
        self.__validate(amount)
        self.__amount = float(amount)

    def __validate(self, amount: Union[int, float]) -> None:
        """Validate monetary amount"""
        if not isinstance(amount, (int, float)):
            raise ValueError(f"Amount must be a number, got {type(amount)}")
        if amount < 0:
            raise ValueError(f"Amount cannot be negative: {amount}")
        if isinstance(amount, float) and not isinstance(amount, bool):
            # Check for NaN and infinity
            if amount != amount:  # NaN check
                raise ValueError("Amount cannot be NaN")
            if amount == float('inf') or amount == float('-inf'):
                raise ValueError("Amount cannot be infinite")

    @property
    def value(self) -> float:
        """Get the monetary value as float"""
        return self.__amount

    def __add__(self, other: Union['Money', int, float]) -> 'Money':
        if isinstance(other, Money):
            return Money(self.__amount + other.value)
        return Money(self.__amount + other)

    def __sub__(self, other: Union['Money', int, float]) -> 'Money':
        if isinstance(other, Money):
            return Money(self.__amount - other.value)
        return Money(self.__amount - other)

    def __mul__(self, factor: Union[int, float]) -> 'Money':
        return Money(self.__amount * factor)

    def __truediv__(self, divisor: Union[int, float]) -> 'Money':
        return Money(self.__amount / divisor)

    def __lt__(self, other: Union['Money', int, float]) -> bool:
        if isinstance(other, Money):
            return self.__amount < other.value
        return self.__amount < other

    def __le__(self, other: Union['Money', int, float]) -> bool:
        if isinstance(other, Money):
            return self.__amount <= other.value
        return self.__amount <= other

    def __gt__(self, other: Union['Money', int, float]) -> bool:
        if isinstance(other, Money):
            return self.__amount > other.value
        return self.__amount > other

    def __ge__(self, other: Union['Money', int, float]) -> bool:
        if isinstance(other, Money):
            return self.__amount >= other.value
        return self.__amount >= other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Money):
            # Handle floating point
            return abs(self.__amount - other.value) < 0.01
        if isinstance(other, (int, float)):
            return abs(self.__amount - other) < 0.01
        return False

    def __str__(self) -> str:
        return f"${self.__amount:.2f}"

    def __repr__(self) -> str:
        return f"Money({self.__amount})"

    def __float__(self) -> float:
        return self.__amount

    def __format__(self, format_spec: str) -> str:
        """Support f-string formatting like {money:.2f}"""
        if format_spec == '':
            return str(self)
        return format(self.__amount, format_spec)

    def __hash__(self) -> int:
        return hash(self.__amount)
