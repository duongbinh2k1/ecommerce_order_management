"""
Promotion model - moved from order_system.py
Added validation logic as per README requirements
"""
import datetime
from typing import Union
from domain.value_objects.money import Money


class Promotion:
    def __init__(
        self,
        promo_id: int,
        code: str,
        discount_percent: Union[int, float],
        min_purchase: Union[int, float],
        valid_until: datetime.datetime,
        category: str
    ) -> None:
        min_purchase_obj = Money(min_purchase)
        self.__validate(code, discount_percent, min_purchase_obj)

        self.__promo_id: int = promo_id
        self.__code: str = code
        self.__discount_percent: Union[int, float] = discount_percent
        self.__min_purchase: Money = min_purchase_obj
        self.__valid_until: datetime.datetime = valid_until
        self.__category: str = category
        self.__used_count: int = 0

    def __validate(
        self,
        code: str,
        discount_percent: Union[int, float],
        min_purchase: Money
    ) -> None:
        """Validate promotion business rules"""
        if not code or not isinstance(code, str):
            raise ValueError("Promotion code must be a non-empty string")
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percent must be between 0 and 100")
        if min_purchase.value < 0:
            raise ValueError("Minimum purchase cannot be negative")

    @property
    def promo_id(self) -> int:
        return self.__promo_id

    @property
    def code(self) -> str:
        return self.__code

    @property
    def discount_percent(self) -> Union[int, float]:
        return self.__discount_percent

    @property
    def min_purchase(self) -> Money:
        return self.__min_purchase

    @property
    def valid_until(self) -> datetime.datetime:
        return self.__valid_until

    @property
    def category(self) -> str:
        return self.__category

    @property
    def used_count(self) -> int:
        return self.__used_count

    @used_count.setter
    def used_count(self, value: int) -> None:
        self.__used_count = value
