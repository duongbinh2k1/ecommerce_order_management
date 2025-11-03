"""
Money value object - for all monetary values (price, total, discount, etc.)
Used throughout the system for financial calculations
"""
from typing import Union


class Money:
    def __init__(self, amount: Union[int, float]) -> None:
        self.__amount = float(amount)
    
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
            return abs(self.__amount - other.value) < 0.01  # Handle floating point
        if isinstance(other, (int, float)):
            return abs(self.__amount - other) < 0.01
        return False
    
    def __str__(self) -> str:
        return f"${self.__amount:.2f}"
    
    def __repr__(self) -> str:
        return f"Money({self.__amount})"
    
    def __float__(self) -> float:
        return self.__amount
    
    def __hash__(self) -> int:
        return hash(self.__amount)
