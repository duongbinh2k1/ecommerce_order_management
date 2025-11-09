"""
OrderItem model - moved from order_system.py
Added validation logic as per README requirements
"""
from typing import Union
from domain.value_objects.money import Money


class OrderItem:
    def __init__(
        self,
        product_id: int,
        quantity: int,
        unit_price: Union[int, float]
    ) -> None:
        self.__validate(quantity, unit_price)

        self.__product_id: int = product_id
        self.__quantity: int = quantity
        self.__unit_price: Money = Money(unit_price)
        self.__discount_applied: Union[int, float] = 0

    def __validate(self, quantity: int, unit_price: Union[int, float]) -> None:
        """Validate order item business rules"""
        if quantity <= 0:
            raise ValueError("Order quantity must be positive")
        if unit_price < 0:
            raise ValueError("Unit price cannot be negative")

    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def quantity(self) -> int:
        return self.__quantity

    @property
    def unit_price(self) -> Money:
        return self.__unit_price

    @property
    def discount_applied(self) -> Union[int, float]:
        return self.__discount_applied

    @discount_applied.setter
    def discount_applied(self, value: Union[int, float]) -> None:
        self.__discount_applied = value
