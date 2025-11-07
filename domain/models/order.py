"""
Order model - moved from order_system.py
Added validation logic as per README requirements
"""
import datetime
from typing import List, Union, Optional
from domain.enums.order_status import OrderStatus
from domain.enums.payment_method import PaymentMethod
from domain.value_objects.money import Money

# TYPE_CHECKING to avoid circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.models.order_item import OrderItem


class Order:
    def __init__(
        self,
        order_id: int,
        customer_id: int,
        items: List['OrderItem'],
        status: str,
        created_at: datetime.datetime,
        total_price: Union[int, float],
        shipping_cost: Union[int, float]
    ) -> None:
        status_enum = OrderStatus(status)
        total_price_obj = Money(total_price)
        shipping_cost_obj = Money(shipping_cost)

        self.__validate(items, total_price_obj, shipping_cost_obj)

        self.__order_id: int = order_id
        self.__customer_id: int = customer_id
        self.__items: List['OrderItem'] = items
        self.__status: OrderStatus = status_enum
        self.__created_at: datetime.datetime = created_at
        self.__total_price: Money = total_price_obj
        self.__shipping_cost: Money = shipping_cost_obj
        self.__tracking_number: Optional[str] = None
        self.__payment_method: Optional[PaymentMethod] = None

    def __validate(
        self,
        items: List['OrderItem'],
        total_price: Money,
        shipping_cost: Money
    ) -> None:
        """Validate order business rules"""
        if not items:
            raise ValueError("Order must have at least one item")
        if total_price.value < 0:
            raise ValueError("Total price cannot be negative")
        if shipping_cost.value < 0:
            raise ValueError("Shipping cost cannot be negative")

    @property
    def order_id(self) -> int:
        return self.__order_id

    @property
    def customer_id(self) -> int:
        return self.__customer_id

    @property
    def items(self) -> List['OrderItem']:
        return self.__items

    @property
    def status(self) -> OrderStatus:
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        self.__status = OrderStatus(value)

    @property
    def created_at(self) -> datetime.datetime:
        return self.__created_at

    @property
    def total_price(self) -> Money:
        return self.__total_price

    @total_price.setter
    def total_price(self, value: Union[int, float]) -> None:
        value_obj = Money(value)
        if value_obj.value < 0:
            raise ValueError("Total price cannot be negative")
        self.__total_price = value_obj

    @property
    def shipping_cost(self) -> Money:
        return self.__shipping_cost

    @property
    def tracking_number(self) -> Optional[str]:
        return self.__tracking_number

    @tracking_number.setter
    def tracking_number(self, value: Optional[str]) -> None:
        self.__tracking_number = value

    @property
    def payment_method(self) -> Optional[PaymentMethod]:
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, value: Optional[str]) -> None:
        if value is not None:
            self.__payment_method = PaymentMethod(value)
        else:
            self.__payment_method = None
