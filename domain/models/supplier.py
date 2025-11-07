"""
Supplier model - moved from order_system.py
Added validation logic as per README requirements
"""
from typing import Union
from domain.value_objects.email import Email


class Supplier:
    def __init__(
        self,
        supplier_id: int,
        name: str,
        email: str,
        reliability_score: Union[int, float]
    ) -> None:
        self.__validate(name, reliability_score)

        self.__supplier_id: int = supplier_id
        self.__name: str = name
        self.__email: Email = Email(email)
        self.__reliability_score: Union[int, float] = reliability_score

    def __validate(
        self,
        name: str,
        reliability_score: Union[int, float]
    ) -> None:
        """Validate supplier business rules"""
        if not name or not isinstance(name, str):
            raise ValueError("Supplier name must be a non-empty string")
        if reliability_score < 0 or reliability_score > 5:
            raise ValueError("Reliability score must be between 0 and 5")

    @property
    def supplier_id(self) -> int:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> Email:
        return self.__email

    @property
    def reliability_score(self) -> Union[int, float]:
        return self.__reliability_score

    @reliability_score.setter
    def reliability_score(self, value: Union[int, float]) -> None:
        if value < 0 or value > 5:
            raise ValueError("Reliability score must be between 0 and 5")
        self.__reliability_score = value
