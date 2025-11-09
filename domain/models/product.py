"""
Product model - moved from order_system.py
Added validation logic as per README requirements
"""
from typing import Union
from domain.value_objects.money import Money


class Product:
    def __init__(
        self,
        product_id: int,
        name: str,
        price: Union[int, float],
        quantity_available: int,
        category: str,
        weight: Union[int, float],
        supplier_id: int
    ) -> None:
        self.__validate(name, price, quantity_available, weight)

        self.__product_id: int = product_id
        self.__name: str = name
        self.__price: Money = Money(price)
        self.__quantity_available: int = quantity_available
        self.__category: str = category
        self.__weight: Union[int, float] = weight
        self.__supplier_id: int = supplier_id
        self.__discount_eligible: bool = True

    def __validate(
        self,
        name: str,
        price: Union[int, float],
        quantity_available: int,
        weight: Union[int, float]
    ) -> None:
        """Validate product business rules"""
        if not name or not isinstance(name, str):
            raise ValueError("Product name must be a non-empty string")
        if price < 0:
            raise ValueError("Product price cannot be negative")
        if quantity_available < 0:
            raise ValueError("Product quantity cannot be negative")
        if weight < 0:
            raise ValueError("Product weight cannot be negative")

    @property
    def product_id(self) -> int:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> Money:
        return self.__price

    @price.setter
    def price(self, value: Union[int, float]) -> None:
        value_obj = Money(value)
        if value_obj.value < 0:
            raise ValueError("Product price cannot be negative")
        self.__price = value_obj

    @property
    def quantity_available(self) -> int:
        return self.__quantity_available

    @quantity_available.setter
    def quantity_available(self, value: int) -> None:
        if value < 0:
            raise ValueError("Product quantity cannot be negative")
        self.__quantity_available = value

    @property
    def category(self) -> str:
        return self.__category

    @property
    def weight(self) -> Union[int, float]:
        return self.__weight

    @property
    def supplier_id(self) -> int:
        return self.__supplier_id

    @property
    def discount_eligible(self) -> bool:
        return self.__discount_eligible

    @discount_eligible.setter
    def discount_eligible(self, value: bool) -> None:
        self.__discount_eligible = value
